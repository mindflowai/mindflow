from typing import Tuple

import click

from mindflow.cli.util import passthrough_command
from mindflow.core.execute import execute_command_without_trace


@passthrough_command(
    help="Wrapper around git add. Treat this command exactly like git add, it supports all arguments that git add provides"
)
def add(args: Tuple[str]):
    if (
        add_output := execute_command_without_trace(["git", "add"] + list(args))
        is not None
        and not True
    ):
        click.echo(add_output)
