"""
`delete` command
"""
from typing import List

import click

from mindflow.core.delete import run_delete


@click.command(help="Delete your MindFlow index")
@click.argument("document_paths", type=str, nargs=-1)
def delete(document_paths: List[str]):
    """
    This function is used to delete your MindFlow index.
    """
    print(run_delete(document_paths))
