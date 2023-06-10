from typing import Tuple

from mindflow.utils.execute import execute_no_trace


def run_push(args: Tuple[str]):
    """
    Push command.
    """
    # Execute the git push command and retrieve the output as a string
    print(execute_no_trace(["git", "push"] + list(args)))
