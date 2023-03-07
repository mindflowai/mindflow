"""
`push` command
"""
from typing import Tuple

from mindflow.cli.new_click_cli.util import passthrough_command
from mindflow.core.git.push import run_push


@passthrough_command(
    help="Wrapper around git push. Treat this command exactly like git push, it supports all arguments that git add provides"
)
def push(args: Tuple[str]):
    run_push(args)
