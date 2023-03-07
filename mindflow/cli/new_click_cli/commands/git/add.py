"""
`add` command
"""
from typing import Tuple

from mindflow.cli.new_click_cli.util import passthrough_command
from mindflow.core.git.add import run_add


@passthrough_command(
    help="Wrapper around git add. Treat this command exactly like git add, it supports all arguments that git add provides"
)
def add(args: Tuple[str]):
    run_add(args)
