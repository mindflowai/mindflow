"""
`diff` command
"""

import click
from mindflow.core.diff import run_diff

@click.command(help="Wrapper around git diff that summarizes the output. Treat this command exactly like git diff, it supports all arguments that git diff provides.")
@click.argument("args", type=str, nargs=-1)
def diff(args: str) -> str:
    command = ['git', 'diff'] + list(args)
    run_diff(command)
