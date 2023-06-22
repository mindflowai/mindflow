import json
from typing import List

from mindflow.core.types.document import (
    Document,
    DocumentChunk,
    DocumentReference,
    get_document_chunk_ids,
    get_document_id,
)
from mindflow.core.resolving.resolve import resolve_paths_to_document_references


def run_inspect(document_paths: List[str]) -> str:
    document_references: List[DocumentReference] = resolve_paths_to_document_references(
        document_paths
    )
    document_ids = document_ids = [
        document_id
        for document_reference in document_references
        if (
            document_id := get_document_id(
                document_reference.path, document_reference.document_type
            )
        )
        is not None
    ]

    if not (
        document_chunk_ids := get_document_chunk_ids(
            Document.load_bulk_ignore_missing(document_ids)
        )
    ):
        return "No documents to inspect"

    document_chunks: List[DocumentChunk] = DocumentChunk.load_bulk_ignore_missing(
        document_chunk_ids
    )

    inspect_output = json.dumps(
        {
            document_chunk.id: {
                k: v for k, v in document_chunk.__dict__.items() if k != "embedding"
            }
            for document_chunk in document_chunks
            if document_chunk is not None
        },
        indent=4,
    )

    if inspect_output != "null":
        return inspect_output
    return "No documents to inspect"
