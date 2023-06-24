import asyncio
from typing import List
import click
from result import Result

from mindflow.core.commands.inspect import run_inspect
from mindflow.core.resolving.resolve import resolve_paths_to_document_references
from mindflow.core.types.document import DocumentReference, get_document_id


@click.command(help="Inspect your MindFlow index")
@click.argument("document_paths", type=str, nargs=-1)
def inspect(document_paths: List[str]):
    document_references: List[DocumentReference] = resolve_paths_to_document_references(
        document_paths
    )
    document_ids: List[str] = [
        document_id
        for document_reference in document_references
        if (
            document_id := get_document_id(
                document_reference.path, document_reference.document_type
            )
        )
        is not None
    ]
    inspect_result: Result[str, str] = asyncio.run(run_inspect(document_ids))
    click.echo(inspect_result.value)
