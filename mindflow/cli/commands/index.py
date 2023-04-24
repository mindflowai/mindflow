"""
`generate` command
"""
from typing import List

import click

from mindflow.core.index import run_index


@click.command(
    help="Index path(s). You can pass as many folders/files/paths as you'd like. Pass `.` to reference all "
)
@click.argument("document_paths", type=str, nargs=-1, required=True)
@click.option("--refresh", is_flag=True, default=False)
def index(document_paths: List[str], refresh: bool) -> None:
    run_index(document_paths, refresh)
