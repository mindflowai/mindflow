from typing import Tuple

import click

from mindflow.cli.util import passthrough_command
from mindflow.core.execute import execute_command_without_trace


@passthrough_command(
    help="Wrapper around git push. Treat this command exactly like git push, it supports all arguments that git add provides"
)
def push(args: Tuple[str]):
    if (
        push_output := execute_command_without_trace(["git", "push"] + list(args))
        is not None
        and not True
    ):
        click.echo(push_output)
