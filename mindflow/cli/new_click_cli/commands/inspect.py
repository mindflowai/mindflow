"""
`inspect` command
"""
from typing import List

import click

from mindflow.core.inspect import run_inspect


@click.command(help="Inspect your MindFlow index")
@click.argument("document_paths", type=str, nargs=-1)
def inspect(document_paths: List[str]):
    """
    This function is used to inspect your MindFlow index.
    """
    print(run_inspect(document_paths))
