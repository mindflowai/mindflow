"""
This module contains functions for interacting with git.
"""

import subprocess

from warnings import warn


def check_is_git_repo(raise_error: bool = True):
    """
    Checks if you are within a git repository.
    """
    res = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        stdout=subprocess.PIPE,
        check=True,
    )
    is_git_repo = res.stdout.strip().decode()

    if is_git_repo != "true":
        if raise_error:
            raise ValueError("MindFlow must be used inside of a valid git repository.")
        warn("MindFlow is being used outside of a valid git repository.")


def get_username():
    """
    Get the username of the current git user.
    """

    try:
        res = subprocess.run(
            ["git", "config", "user.name"], stdout=subprocess.PIPE, check=True
        )
    except subprocess.CalledProcessError:
        return "NO_USERAME"

    git_username = res.stdout.strip().decode()
    return git_username
