from typing import Tuple

from mindflow.core.execute import execute_command_and_print_without_trace


def run_add(args: Tuple[str]):
    execute_command_and_print_without_trace(["git", "add"] + list(args))
