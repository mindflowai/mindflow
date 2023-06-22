import logging
import os
from typing import List

from mindflow.core.file_processing.git import (
    is_path_within_git_repo,
    get_all_unignored_git_files_from_path,
)


def extract_files_from_directory(path) -> List[str]:
    file_paths = []
    if os.path.isfile(path):
        return [os.fspath(path)]
    if is_path_within_git_repo(path):
        return get_all_unignored_git_files_from_path(path)
    try:
        with os.scandir(path) as paths:
            for scanned_path in paths:
                if scanned_path.is_file():
                    file_paths.append(os.path.abspath(scanned_path.path))
                elif os.path.isdir(path):
                    file_paths.extend(extract_files_from_directory(scanned_path.path))
        return file_paths
    except IsADirectoryError as error:
        logging.debug("Could not read directory/file: %s", path)
        logging.debug(error)
        return file_paths
