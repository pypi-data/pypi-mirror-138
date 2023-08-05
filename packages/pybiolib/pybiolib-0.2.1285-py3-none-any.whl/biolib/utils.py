import multiprocessing
import os
import time
from urllib.parse import urlparse

import requests
from importlib_metadata import version, PackageNotFoundError

# try fetching version, if it fails (usually when in dev), add default
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger

try:
    BIOLIB_PACKAGE_VERSION = version('pybiolib')
except PackageNotFoundError:
    BIOLIB_PACKAGE_VERSION = '0.0.0'

IS_DEV = os.getenv('BIOLIB_DEV', '').upper() == 'TRUE'

BIOLIB_PACKAGE_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BIOLIB_CLOUD_ENVIRONMENT = os.getenv('BIOLIB_CLOUD_ENVIRONMENT', '').lower()

BIOLIB_IS_RUNNING_IN_ENCLAVE = BIOLIB_CLOUD_ENVIRONMENT == 'enclave'

IS_RUNNING_IN_CLOUD = BIOLIB_CLOUD_ENVIRONMENT in ('enclave', 'non-enclave')

if BIOLIB_CLOUD_ENVIRONMENT and not IS_RUNNING_IN_CLOUD:
    logger.warning((
        'BIOLIB_CLOUD_ENVIRONMENT defined but does not specify the cloud environment correctly. ',
        'The compute node will not act as a cloud compute node'
    ))

BIOLIB_CLOUD_SKIP_PCR_VERIFICATION = os.getenv('BIOLIB_CLOUD_SKIP_PCR_VERIFICATION', '').upper() == 'TRUE'

BIOLIB_ENABLE_DNS_PROXY = os.getenv('BIOLIB_ENABLE_DNS_PROXY', '').upper() == 'TRUE'

RUN_DEV_JOB_ID = 'run-dev-mocked-job-id'


def get_absolute_container_image_uri(base_url: str, relative_image_uri: str, job_is_federated: bool = False):
    if base_url == 'https://biolib.com' or job_is_federated:
        container_registry_hostname = 'containers.biolib.com'
    elif base_url in ('https://staging-elb.biolib.com', 'https://staging.biolib.com'):
        container_registry_hostname = 'containers.staging.biolib.com'
    else:
        # Expect registry to be accessible on the hostname of base_url if not running on biolib.com
        base_hostname = urlparse(base_url).hostname
        if not base_hostname:
            raise Exception("Could not get hostname from base_url. Tried to get ecr_proxy_uri for image pulling.")
        container_registry_hostname = base_hostname

    return f'{container_registry_hostname}/{relative_image_uri}'


def _download_chunk(input_tuple):
    start, end, presigned_url = input_tuple
    max_upload_retries = 5

    for retry_attempt in range(max_upload_retries):
        logger.debug(f'Attempt number {retry_attempt} for part {start}')
        try:
            response = requests.get(
                url=presigned_url,
                stream=True,
                headers={'range': f'bytes={start}-{end}'},
                timeout=300,  # timeout after 5 min
            )
            if response.ok:
                return_value = response.raw.data
                logger.debug(f'Returning raw data for part {start}')
                return return_value
            else:
                logger.warning(f'Got not ok response when downloading part {start}:{end}. Retrying...')
        except Exception:  # pylint: disable=broad-except
            logger.warning(f'Encountered error when downloading part {start}:{end}. Retrying...')

        time.sleep(2)

    logger.debug(f'Max retries hit, when downloading part {start}:{end}. Exiting...')
    raise BioLibError(f'Max retries hit, when downloading part {start}:{end}. Exiting...')


def download_presigned_s3_url(presigned_url: str, output_file_path: str) -> None:
    chunk_size = 50_000_000

    with requests.get(presigned_url, stream=True, headers={'range': 'bytes=0-1'}) as response:
        file_size = int(response.headers['Content-Range'].split('/')[1])

    chunk_iterator = [(i, i + chunk_size - 1, presigned_url) for i in range(0, file_size, chunk_size)]

    process_pool = multiprocessing.Pool(
        # use 8 cores, unless less is available
        processes=min(16, multiprocessing.cpu_count() - 1),
    )

    bytes_written = 0

    with open(output_file_path, 'ab') as output_file:
        for index, data in enumerate(process_pool.imap(_download_chunk, chunk_iterator)):
            logger.debug(f'Writing part {index} of {file_size} to file...')
            output_file.write(data)

            bytes_written += chunk_size
            approx_progress_percent = min(bytes_written / file_size * 100, 100)
            logger.debug(
                f'Wrote part {index} of {file_size} to file, '
                f'the approximate progress is {round(approx_progress_percent, 2)}%'
            )

    process_pool.close()
