from typing import Tuple

from mindflow.core.execute import execute_command_and_print_without_trace


def run_push(args: Tuple[str]):
    print(execute_command_and_print_without_trace(["git", "push"] + list(args)))
