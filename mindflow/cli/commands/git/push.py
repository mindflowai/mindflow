import click

from typing import Tuple

from mindflow.cli.util import passthrough_command


@passthrough_command(
    help="Wrapper around git push. Treat this command exactly like git push, it supports all arguments that git add provides"
)
def push(args: Tuple[str]):
    from mindflow.cli.util import execute_command_without_trace

    if (
        push_output := execute_command_without_trace(["git", "push"] + list(args))
        is not None
        and not True
    ):
        click.echo(push_output)
