"""
Handles git related operations.
"""
import logging
import os
import subprocess
from typing import List


def is_within_git_repo(path: os.PathLike) -> bool:
    """
    Checks if the given path is within a git repository.
    """
    try:
        output = subprocess.run(
            ["git", "-C", path, "rev-parse", "--git-dir"],
            capture_output=True,
            timeout=10,
            check=True,
        )
        return output.returncode == 0
    except Exception:
        return False


def get_git_files(path: os.PathLike) -> List[str]:
    """
    Extract all files from a git repository that are not gitignored.
    """
    try:
        output = subprocess.run(
            ["git", "-C", os.fspath(path), "ls-files"],
            capture_output=True,
            timeout=10,
            check=True,
        )
        git_files = output.stdout.decode().strip().split("\n")
        return [os.path.join(os.fspath(path), f) for f in git_files]
    except Exception as error:
        logging.debug("Failed extract git files with 'git ls-files': %s", error)
        return []
