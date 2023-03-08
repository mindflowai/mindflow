"""
`diff` command
"""
from typing import Tuple

import click

from mindflow.cli.new_click_cli.util import passthrough_command
from mindflow.core.git.diff import run_diff


@passthrough_command(
    help="Wrapper around git diff that summarizes the output. Treat this command exactly like git diff, it supports all arguments that git diff provides."
)
@click.option("--detailed", is_flag=True, help="Get a more detailed/thorough diff explanation.")
def diff(args: Tuple[str], detailed: bool):
    print(run_diff(args, summarize=not detailed, note_exclusions=True))
