import json
import os
from typing import Tuple

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

std_names = config['standard_names']

url = config['url']

start_value = config['start_value']


def get_aws_config() -> Tuple[str, str, str, str]:
    endpoint_url = os.getenv('S3_URL', 'http://s3-uk-1.sa-catapult.co.uk')
    access_key = os.getenv('S3_ID', 'test_id')
    secret_access_key = os.getenv(
        'S3_KEY', 'ttest_secret')
    s3_bucket = os.getenv('S3_BUCKET', 'csvs-netcdf')
    return endpoint_url, access_key, secret_access_key, s3_bucket
