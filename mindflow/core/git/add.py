import subprocess
from typing import Tuple

from mindflow.utils.execute import execute_no_trace


def run_add(args: Tuple[str]):
    """
    Add command.
    """
    command = ["git", "add"] + list(args)

    # Execute the git diff command and retrieve the output as a string
    execute_no_trace(command)
