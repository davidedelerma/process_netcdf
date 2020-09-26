#!/usr/bin/env python
# coding: utf-8
from pathlib import Path
from shutil import rmtree
from time import sleep

from load_config import start_value, std_names, url
from services.cube_service import merge_all_nc, add_standard_name_to_cube
from services.decompress_service import uncompress_downloaded_tar
from services.html_service import get_html_data_list, download_file
from services.upload_service import make_s3_destination_filename, upload_to_s3


def make_url(base_url: str, filename: str) -> str:
    stripped_url = base_url.rstrip('/')
    return f'{stripped_url}/{filename}'


def make_dest_path(filename: str) -> str:
    cwd = Path.cwd()
    temp = cwd / 'temp'
    temp.mkdir(exist_ok=True)
    return f'{str(temp)}/{filename}'


def wait_for_decompress(filepath: str) -> None:
    while True:
        if len(list(Path(filepath).glob('*.gz'))) == 0:
            break
        print(f'there are still netcdf files to decompress')
        sleep(1)
    print(
        f'decompressed all netcdfs ------------------------------------------')


def make_output_nc_filepath(folder_with_nc: str) -> str:
    cwd = Path.cwd()
    temp = cwd / 'results'
    temp.mkdir(mode=0o777, exist_ok=True)
    base = folder_with_nc.rsplit('/', 1)[0]
    filename = base.rsplit('/', 1)[-1] + '.nc'
    return str(temp) + '/' + filename


def cleanup_folder(folder_path: str) -> None:
    rmtree(folder_path)


def main(url_for_data: str) -> None:
    data_list = get_html_data_list(site=url_for_data)[start_value:]
    print(f'there are {len(data_list)} file to process')
    count = 0
    for data in data_list:
        site = make_url(url_for_data, data)
        dest_path = make_dest_path(filename=data)
        print(f'start downloading {data}')
        downloaded_file = download_file(site=site, dest_path=dest_path)
        print(f'downloaded file {downloaded_file}')
        folder_with_nc = uncompress_downloaded_tar(
            downloaded_file_path=downloaded_file, filename=data)
        wait_for_decompress(folder_with_nc)
        merged_nc_filepath = make_output_nc_filepath(
            folder_with_nc=folder_with_nc)
        merge_all_nc(filepath=folder_with_nc, output_path=merged_nc_filepath)
        add_standard_name_to_cube(
            path_to_file=merged_nc_filepath, std_name_dict=std_names)
        cleanup_folder(folder_path=str(Path(folder_with_nc).parent))
        print(f'processed {count} of {len(data_list)}')
        s3_destination = make_s3_destination_filename(
            url=url_for_data, merged_nc_filepath=merged_nc_filepath)
        print(f'S3 destination: {s3_destination}')
        upload_to_s3(src_path=merged_nc_filepath, dest_path=s3_destination)
        print(
            f'uploaded {count} files of {len(data_list)} '
            f'| file uploaded to destination {s3_destination}')
        Path(downloaded_file).unlink()
        Path(merged_nc_filepath).unlink()
    cleanup_folder(str(Path.cwd() / 'temp'))
    cleanup_folder(str(Path.cwd() / 'unpacked_temp'))
    cleanup_folder(str(Path.cwd() / 'results'))


if __name__ == "__main__":
    main(url_for_data=url)
