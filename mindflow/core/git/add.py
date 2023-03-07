import subprocess
from typing import Tuple


def run_add(args: Tuple[str]):
    """
    Add command.
    """
    command = ["git", "add"] + list(args)

    # Execute the git diff command and retrieve the output as a string
    subprocess.check_output(command).decode("utf-8")
