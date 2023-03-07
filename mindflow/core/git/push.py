import subprocess
from typing import Tuple


def run_push(args: Tuple[str]):
    """
    Push command.
    """
    command = ["git", "push"] + list(args)

    # Execute the git diff command and retrieve the output as a string
    subprocess.check_output(command).decode("utf-8")
