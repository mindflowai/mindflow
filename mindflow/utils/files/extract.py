import logging
import os

from typing import List

from mindflow.utils.files.git import is_within_git_repo, get_git_files


def extract_files(path: os.PathLike) -> List[os.PathLike]:
    """
    Extract all files from a directory.
    """
    file_paths = []
    if os.path.isfile(path):
        return [os.fspath(path)]
    if is_within_git_repo(path):
        return get_git_files(path)
    try:
        with os.scandir(path) as paths:
            for path in paths:
                if path.is_file():
                    file_paths.append(os.fspath(path.path))
                elif path.is_dir():
                    file_paths.extend(extract_files(path.path))
        return file_paths
    except IsADirectoryError as error:
        logging.debug("Could not read directory/file: %s", path)
        logging.debug(error)
        return file_paths
