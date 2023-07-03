import click
from typing import Tuple
from mindflow.cli.util import passthrough_command


@passthrough_command(
    help="Wrapper around git add. Treat this command exactly like git add, it supports all arguments that git add provides"
)
def add(args: Tuple[str]):
    from mindflow.cli.util import execute_command_without_trace

    if (
        add_output := execute_command_without_trace(["git", "add"] + list(args))
        is not None
        and not True
    ):
        click.echo(add_output)
