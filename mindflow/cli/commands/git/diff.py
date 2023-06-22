"""
`diff` command
"""
from typing import Tuple
import click

from mindflow.cli.util import passthrough_command
from mindflow.core.commands.git.diff import run_diff


@passthrough_command(
    help="Wrapper around git diff that summarizes the output. Treat this command exactly like git diff, it supports all arguments that git diff provides."
)
@click.option("--detailed", type=bool, default=False, is_flag=True)
def diff(args: Tuple[str], detailed: bool):
    if not detailed:
        click.echo(
            "Working on a summary of the diff, use the `--detailed` flag to show a much more thorough breakdown of the diff...\n"
        )
    if (diff_output := run_diff(args, detailed=detailed)) is not None:
        click.echo(diff_output)
