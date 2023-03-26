"""
`delete` command
"""
import os
from typing import List, Optional, Tuple

from mindflow.db.objects.document import Document, DocumentChunk, get_document_id
from mindflow.resolving.resolve import resolve_all


def run_delete(document_paths: List[str]):
    """
    This function is used to delete your MindFlow index.
    """
    document_paths = [os.path.abspath(path) for path in document_paths]
    resolved: List[Tuple[str, str]] = resolve_all(document_paths)

    document_ids = [
        get_document_id(doc_path, doc_type) for doc_path, doc_type in resolved
    ]
    documents: List[Optional[Document]] = Document.load_bulk(document_ids)

    if len(documents) == 0:
        return "No documents to delete"

    document_chunk_ids = []
    for document in documents:
        if document is not None:
            document_chunk_ids.extend(
                [f"{document.id}_{i}" for i in range(0, int(document.num_chunks))]
            )

    if len(document_chunk_ids) == 0:
        return "No documents to delete"

    document_chunks: List[Optional[DocumentChunk]] = DocumentChunk.load_bulk(
        document_chunk_ids
    )
    output = {}
    for document_chunk in document_chunks:
        if document_chunk is not None:
            output.update(document_chunk.todict(document_chunk))

    Document.delete_bulk(document_ids)
    DocumentChunk.delete_bulk(document_chunk_ids)

    return "Documents deleted"
