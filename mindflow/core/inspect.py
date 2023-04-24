"""
`inspect` command
"""
import json
from typing import List, Optional, Tuple

from mindflow.db.objects.document import (
    Document,
    DocumentChunk,
    get_document_chunk_ids,
    get_document_id,
)
from mindflow.resolving.resolve import resolve_all


def run_inspect(document_paths: List[str]) -> str:
    """
    This function is used to inspect your MindFlow index.
    """
    resolved: List[Tuple[str, str]] = resolve_all(document_paths)

    document_ids = [
        document_id
        for document_id in [
            get_document_id(doc_path, doc_type) for doc_path, doc_type in resolved
        ]
        if document_id is not None
    ]
    document_chunk_ids = get_document_chunk_ids(
        Document.load_bulk(document_ids, return_none=False)
    )

    if len(document_chunk_ids) == 0:
        return "No documents to inspect"

    document_chunks: List[Optional[DocumentChunk]] = DocumentChunk.load_bulk(
        document_chunk_ids, return_none=False
    )

    # Dump the document chunks to JSON without the embedding
    inspect_output = json.dumps(
        {
            document_chunk.id: {
                k: v
                for k, v in document_chunk.todict(document_chunk).items()
                if k != "embedding"
            }
            for document_chunk in document_chunks
            if document_chunk is not None
        },
        indent=4,
    )

    if inspect_output != "null":
        return inspect_output
    else:
        return "No documents to inspect"
