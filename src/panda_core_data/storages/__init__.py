from pathlib import Path
from typing import List, Iterator

from ..custom_typings import PathType
from ..custom_exceptions import PCDInvalidPath, PCDRawFileNotSupported


try:
    from .base_db import available_storages
    from .json_db import JsonDB
    from .yaml_db import YamlDB
# I did some testing and yaml doesn't work with python.net
except TypeError:  # pragma: no cover
    print("Yaml might be not supported")


def get_raw_extensions() -> List[str]:
    """Get all available extensions the package supports

    :return: A list of available extensions"""
    return [ext for ext_dict in available_storages
            for ext in ext_dict['extensions']]


def get_extension(path: PathType) -> str:
    """Get file extension from the path

    :param path: path to a file or extension
    :return: The file extension"""
    if isinstance(path, Path):
        extension = path.suffix
    else:
        path = str(path)
        if "\\" in path or "/" in path or "." in path:
            extension = auto_convert_to_pathlib(path).suffix
        else:
            extension = path

    return extension.replace(".", "")


def get_storage_from_extension(extension: str) -> "tinydb.storages.Storage":
    """Returns the storage based on the file extension

    :return: Returns a storage object that handles the raw file"""
    for storage_dict in available_storages:
        if extension in storage_dict["extensions"]:
            return storage_dict["storage"]

    raise PCDRawFileNotSupported(f"The extension {extension} is not supported "
                                 "for raws, the  available extensions are " +
                                 str(get_raw_extensions()))


def raw_glob_iterator(path: PathType, excluded_ext: bool = False
                      ) -> Iterator[Path]:
    """Iterate along the path yielding the raw file.

    :yields: The file"""
    path = auto_convert_to_pathlib(path)

    for ext in get_raw_extensions():
        for file in path.glob(f'*.{ext}'):
            if (not excluded_ext) or (ext not in excluded_ext):
                yield file


def is_excluded_extension(path: PathType, exclude_ext: List[str]) -> bool:
    """Check if the file has an ignored extension

    :param path: source folder
    :param exclude_ext: If the path should be from a folder or file
    :return: returns True if it's a excluded extension, False otherwise"""
    if exclude_ext and get_extension(path) in exclude_ext:
        return True
    return False


def auto_convert_to_pathlib(path: PathType) -> Path:
    """Check if the path is valid and automatically convert it into a Path
    object

    :param path: source folder
    :return: The Path object
    :raise PCDInvalidPath: If the file is invalid"""
    if not isinstance(path, Path):
        path = Path(path)

    if path.is_file() or path.is_dir():
        return path

    raise PCDInvalidPath(f"The file {path} could not be found.")
