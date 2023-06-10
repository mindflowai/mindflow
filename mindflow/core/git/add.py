from typing import Tuple

from mindflow.utils.execute import execute_no_trace


def run_add(args: Tuple[str]):
    """
    Add command.
    """
    # Execute the git add command and retrieve the output as a string
    execute_no_trace(["git", "add"] + list(args))
