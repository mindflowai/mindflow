import asyncio
from typing import List

import click
from result import Result

from mindflow.core.commands.delete import run_delete
from mindflow.core.resolving.resolve import resolve_paths_to_document_references
from mindflow.core.types.document import DocumentReference, get_document_id


@click.command(help="Delete your MindFlow index")
@click.argument("document_paths", type=str, nargs=-1)
def delete(document_paths: List[str]):
    document_references: List[DocumentReference] = resolve_paths_to_document_references(
        document_paths
    )

    document_ids = [
        document_id
        for document_id in [
            get_document_id(document_reference.path, document_reference.document_type)
            for document_reference in document_references
        ]
        if document_id is not None
    ]

    delete_result: Result[str, str] = asyncio.run(run_delete(document_ids))
    click.echo(delete_result.value)
