import os
import sys
import threading

import boto3

from src.config import get_aws_config


def upload_to_s3(src_path: str, dest_path: str) -> None:
    endpoint_url, access_key, secret_access_key, s3_bucket = get_aws_config()
    print(f'access key; {access_key}, secret access key: {secret_access_key}')
    print(f'starting uploading {src_path}')
    s3 = boto3.client('s3', endpoint_url=endpoint_url,
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_access_key)
    s3.upload_file(src_path, s3_bucket, dest_path,
                   Callback=ProgressPercentage(src_path))
    print(f'Uploaded {src_path} to S3 as {dest_path}')


def make_s3_destination_filename(url: str, merged_nc_filepath: str) -> str:
    data_recurrence = url.rsplit('/', 1)[-1]
    merged_nc_filename = merged_nc_filepath.rsplit('/', 1)[-1]
    return data_recurrence + '/' + merged_nc_filename


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()
