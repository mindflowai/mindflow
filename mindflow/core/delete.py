"""
`delete` command
"""
from typing import List, Optional, Tuple

from mindflow.db.objects.document import (
    Document,
    DocumentChunk,
    get_document_chunk_ids,
    get_document_id,
)
from mindflow.resolving.resolve import resolve_all


def run_delete(document_paths: List[str]):
    """
    This function is used to delete your MindFlow index.
    """
    resolved: List[Tuple[str, str]] = resolve_all(document_paths)

    document_ids = [
        document_id
        for document_id in [
            get_document_id(doc_path, doc_type) for doc_path, doc_type in resolved
        ]
        if document_id is not None
    ]
    documents: List[Document] = Document.load_bulk(document_ids, return_none=False)
    if len(documents) == 0:
        return "No documents to delete"

    document_chunk_ids = get_document_chunk_ids(documents)
    document_chunks: List[Optional[DocumentChunk]] = DocumentChunk.load_bulk(
        document_chunk_ids,
        return_none=True,
    )
    if len(document_chunks) == 0:
        return "No documents to delete"

    Document.delete_bulk(document_ids)
    DocumentChunk.delete_bulk(document_chunk_ids)

    return "Documents deleted"
