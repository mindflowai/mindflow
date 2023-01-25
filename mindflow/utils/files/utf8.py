"""
Quick UTF-8 validation.
"""
import codecs
import os


def is_valid_utf8(file_path: os.PathLike) -> bool:
    """
    Check if a file is valid utf8.
    """
    try:
        with codecs.open(file_path, encoding="utf-8", errors="strict") as file:
            for _ in file:
                pass
        return True
    except UnicodeDecodeError:
        return False
