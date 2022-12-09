import gzip
import os
import tarfile
from pathlib import Path
from typing import Optional, Generator


def unpack_tar_file(compressed_file: str, destination: str) -> None:
    if len(os.listdir(destination)) > 0:
        print(
            f'file {compressed_file} already unpacked '
            f'in destination {destination}')
        return
    with tarfile.open(compressed_file, mode='r:gz') as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, path=destination)
    print(f'file extracted in {destination}')


def uncompress_downloaded_tar(downloaded_file_path: str, filename: str) -> str:
    dest_unpacked = make_unpacked_folder(filename=filename)
    unpack_tar_file(compressed_file=downloaded_file_path,
                    destination=dest_unpacked)
    child_unpacked = get_child_unpacked_folder(unpacked_folder=dest_unpacked)
    for nc_file in get_zipped_nc_file(child_unpacked):
        _ = unzip_nc_file(str(nc_file))
        _ = delete_compressed_nc_file(str(nc_file))
    print(f'nc files unzipped in folder {dest_unpacked}')
    return child_unpacked


def delete_compressed_nc_file(filepath: str) -> Optional[str]:
    if filepath.endswith('.gz'):
        os.remove(filepath)
        return filepath
    else:
        raise ValueError(f'file; {filepath} is not compressed')


def unzip_nc_file(filepath: str) -> str:
    with gzip.open(filepath, 'rb') as f:
        output_filepath = filepath.rstrip('.gz')
        with open(output_filepath, 'wb') as w:
            while True:
                piece = f.read(1024)
                if not piece:
                    break
                w.write(piece)
    return output_filepath


def make_unpacked_folder(filename: str) -> str:
    filename = filename.rstrip('.tar.gz')
    cwd = Path.cwd()
    temp = cwd / 'unpacked_temp' / filename
    temp.mkdir(mode=0o777, parents=True, exist_ok=True)
    return str(temp)


def get_child_unpacked_folder(unpacked_folder: str) -> str:
    list_dir = os.listdir(unpacked_folder)
    if len(list_dir) != 1:
        raise ValueError(
            f'{unpacked_folder} contains more than a child or is empty')
    return unpacked_folder + '/' + list_dir[0]


def get_zipped_nc_file(folder: str) -> Generator[Path, None, None]:
    return Path(folder).glob('*.gz')
