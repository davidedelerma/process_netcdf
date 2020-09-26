import os
from typing import Tuple

std_names = {
    '2 metre temperature': 'surface_temperature',
    'Total precipitation': 'precipitation_flux',
    'Sea surface temperature': 'sea_surface_temperature',
    'Soil temperature level 1': 'soil_temperature',
    'Volumetric soil water layer 1': 'volume_fraction_of_condensed_water_in_soil',
    'precipitation rate': 'precipitation_rate'
}

url = 'http://37.128.186.209/LAURA/ERA5/30year'

start_value = int(os.getenv('START_ITERATION', '0'))


def get_aws_config() -> Tuple[str, str, str, str]:
    endpoint_url = os.getenv('S3_URL', 'http://s3-uk-1.sa-catapult.co.uk')
    access_key = os.getenv('S3_ID', 'test_id')
    secret_access_key = os.getenv(
        'S3_KEY', 'ttest_secret')
    s3_bucket = os.getenv('S3_BUCKET', 'csvs-netcdf')
    return endpoint_url, access_key, secret_access_key, s3_bucket
