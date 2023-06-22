from typing import List

import click

from mindflow.core.commands.delete import run_delete


@click.command(help="Delete your MindFlow index")
@click.argument("document_paths", type=str, nargs=-1)
def delete(document_paths: List[str]):
    print(run_delete(document_paths))
