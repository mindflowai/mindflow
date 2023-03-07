import click

from typing import Tuple
from mindflow.core.commit import run_commit
from mindflow.cli.new_click_cli.util import passthrough_command


@passthrough_command(help="Generate a git commit response by feeding git diff to gpt")
@click.option(
    "-m",
    "--message",
    help="Don't use mindflow to generate a commit message, use this one instead.",
    default=None,
)
def commit(args: Tuple[str], message: str = None):
    """
    Commit command.
    """

    if message is not None:
        click.echo(
            f"Warning: Using message '{message}' instead of mindflow generated message."
        )
        click.echo("It's recommended that you don't use the -m/--message flag.")

    print(run_commit(args, message_overwrite=message))
