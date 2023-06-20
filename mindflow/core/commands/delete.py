from typing import List

from mindflow.core.types.document import (
    Document,
    DocumentChunk,
    DocumentReference,
    get_document_chunk_ids,
    get_document_id,
)
from mindflow.core.resolving.resolve import resolve_paths_to_document_references


def run_delete(document_paths: List[str]) -> str:
    """Delete documents from MindFlow index."""
    document_references: List[DocumentReference] = resolve_paths_to_document_references(document_paths)

    document_ids = [document_id for document_id in [get_document_id(document_reference.path, document_reference.document_type) for document_reference in document_references] if document_id is not None]

    if not document_ids:
        return "No document IDs resolved. Nothing to delete."

    documents = Document.load_bulk_ignore_missing(document_ids)
    if not documents:
        return "No documents found to delete."

    document_chunk_ids = get_document_chunk_ids(documents)
    if not DocumentChunk.load_bulk_ignore_missing(document_chunk_ids):
        return "No document chunks found to delete."

    Document.delete_bulk(document_ids)
    DocumentChunk.delete_bulk(document_chunk_ids)

    return True, "Documents and associated chunks deleted successfully."
