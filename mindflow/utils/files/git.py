"""
Handles git related operations.
"""
import logging
import os
import subprocess
from typing import List, Union


class NotInGit(BaseException):
    """
    Raised when the given path is not within a git repository.
    """


class GitError(BaseException):
    """
    Raised when a git command fails.
    """


def is_within_git_repo(path: Union[str, os.PathLike]) -> bool:
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
    except NotInGit:
        return False


def get_git_files(path: Union[str, os.PathLike]) -> List[str]:
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
        return [os.path.abspath(os.path.join(os.fspath(path), f)) for f in git_files]
    except GitError as error:
        logging.debug("Failed extract git files with 'git ls-files': %s", error)
        return []
