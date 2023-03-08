from typing import Tuple, Optional

import click

from mindflow.cli.new_click_cli.util import passthrough_command
from mindflow.core.git.commit import run_commit


@passthrough_command(help="Generate a git commit response by feeding git diff to gpt")
# @overloaded_option(
#     "-m",
#     "--message",
#     help="Don't use mindflow to generate a commit message, use this one instead.",
#     default=None,
# )
@click.option(
    "-m",
    "--message",
    help="Don't use mindflow to generate a commit message, use this one instead.",
    default=None,
)
def commit(args: Tuple[str], message: Optional[str] = None):
    """
    Commit command.
    """
    if message is not None:
        click.echo(
            f"Warning: Using message '{message}' instead of mindflow generated message."
        )
        click.echo("It's recommended that you don't use the -m/--message flag.")

    print(run_commit(args, message_overwrite=message))
