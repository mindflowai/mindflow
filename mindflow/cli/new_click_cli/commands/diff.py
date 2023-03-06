"""
`diff` command
"""

import click
from mindflow.core.diff import run_diff

@click.command(help="Generate a git diff response by feeding git diff to gpt")
def diff() -> str:
    run_diff()
