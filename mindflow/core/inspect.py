"""
`inspect` command
"""
import json
import os
from typing import List, Optional, Tuple

from mindflow.db.objects.document import Document, DocumentChunk, get_document_id
from mindflow.resolving.resolve import resolve_all


def run_inspect(document_paths: List[str]) -> str:
    """
    This function is used to inspect your MindFlow index.
    """

    document_paths = [os.path.abspath(path) for path in document_paths]
    resolved: List[Tuple[str, str]] = resolve_all(document_paths)

    document_ids = [
        get_document_id(doc_path, doc_type) for doc_path, doc_type in resolved
    ]
    documents: List[Optional[Document]] = Document.load_bulk(document_ids)

    document_chunk_ids = []
    for document in documents:
        if document is not None:
            document_chunk_ids.extend(
                [f"{document.id}_{i}" for i in range(0, int(document.num_chunks))]
            )

    if len(document_chunk_ids) == 0:
        return "No documents to inspect"

    document_chunks: List[Optional[DocumentChunk]] = DocumentChunk.load_bulk(
        document_chunk_ids
    )
    output = {}
    for document_chunk in document_chunks:
        if document_chunk is not None:
            del document_chunk.embedding
            output[document_chunk.id] = document_chunk.todict(document_chunk)

    inspect_output = json.dumps(
        output,
        indent=4,
    )

    if inspect_output != "null":
        return inspect_output
    else:
        return "No documents to inspect"
