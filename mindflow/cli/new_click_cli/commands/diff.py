"""
`diff` command
"""
from typing import Tuple

from mindflow.core.diff import run_diff
from mindflow.cli.new_click_cli.util import passthrough_command


@passthrough_command(
    help="Wrapper around git diff that summarizes the output. Treat this command exactly like git diff, it supports all arguments that git diff provides."
)
def diff(args: Tuple[str]):
    print(run_diff(args))
