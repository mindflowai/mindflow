from typing import Tuple

from mindflow.core.execute import execute_no_trace


def run_add(args: Tuple[str]):
    execute_no_trace(["git", "add"] + list(args))
