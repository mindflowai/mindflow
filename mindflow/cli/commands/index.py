from typing import List
import click

from mindflow.core.commands.index import run_index
from mindflow.core.settings import Settings


@click.command(
    help="Index path(s). You can pass as many folders/files/paths as you'd like. Pass `.` to reference all "
)
@click.argument("document_paths", type=str, nargs=-1, required=True)
@click.option("--refresh", is_flag=True, default=False)
def index(document_paths: List[str]) -> None:
    print(run_index(Settings(), document_paths))
