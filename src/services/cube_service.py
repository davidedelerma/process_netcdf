from pathlib import Path

import iris
from iris.experimental.equalise_cubes import equalise_attributes


def merge_all_nc(filepath: str, output_path: str) -> str:
    nc_gen = Path(filepath).glob('*.nc')
    cube_list = []
    for nc in nc_gen:
        cube_to_merge = iris.load_cube(str(nc))
        cube_list.append(cube_to_merge)
    merged_cube = merge_cubes(iris.cube.CubeList(cube_list))
    iris.save(merged_cube, output_path)
    print(f'saved merged nc file in {output_path}')
    return output_path


def merge_cubes(cube_list):
    equalise_attributes(cube_list)
    return cube_list.merge_cube()


def add_standard_name_to_cube(path_to_file: str, std_name_dict: dict) -> str:
    original_cube = iris.load_cube(path_to_file)
    print(original_cube)
    if original_cube.standard_name is not None:
        return path_to_file
    std_name = std_name_dict[original_cube.long_name]
    temp_out = path_to_file.rsplit('/', 1)[0] + '/' + std_name + '.nc'
    print(temp_out)
    original_cube.standard_name = std_name
    iris.save(original_cube, temp_out)
    Path(path_to_file).unlink()
    Path(temp_out).rename(path_to_file)
    print(f'added std name {std_name} to {path_to_file}')
    return path_to_file