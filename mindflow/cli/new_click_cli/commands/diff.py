"""
`diff` command
"""

from typing import Tuple
import click
from mindflow.core.diff import run_diff

@click.command(context_settings=dict(
    ignore_unknown_options=True,
), help="Wrapper around git diff that summarizes the output. Treat this command exactly like git diff, it supports all arguments that git diff provides.")
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def diff(args: Tuple[str]) -> str:
    print(run_diff(args))

