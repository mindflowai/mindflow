import subprocess
from typing import Tuple

from mindflow.utils.execute import execute_no_trace


def run_push(args: Tuple[str]):
    """
    Push command.
    """
    command = ["git", "push"] + list(args)

    # Execute the git diff command and retrieve the output as a string
    print(execute_no_trace(command))
