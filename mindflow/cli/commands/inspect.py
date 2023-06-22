from typing import List
import click

from mindflow.core.commands.inspect import run_inspect


@click.command(help="Inspect your MindFlow index")
@click.argument("document_paths", type=str, nargs=-1)
def inspect(document_paths: List[str]):
    print(run_inspect(document_paths))
