"""
This module contains validation functions.
"""

import os

from typing import List


MAX_LENGTH = 20_000


def validate_files_total_length(files: List[str]):
    """
    Validates that the total length/size of the files is less than MAX_LENGTH.
    """
    total_size = 0
    for filename in files:
        file_stat = os.stat(filename)
        total_size += file_stat.st_size

    if total_size > MAX_LENGTH:
        raise ValueError(
            f"File lengths total to {total_size}, but max length is {MAX_LENGTH}. \
                Try restricting the number of files, currently the ones being used are: {files}"
        )
