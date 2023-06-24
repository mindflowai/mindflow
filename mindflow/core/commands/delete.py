import asyncio
from typing import List

from result import Err, Ok, Result

from mindflow.core.types.document import (
    Document,
    DocumentChunk,
    get_document_chunk_ids,
)


async def run_delete(document_ids: List[str]) -> Result[str, str]:
    """Delete documents from MindFlow index."""
    documents = await Document.load_bulk_ignore_missing(document_ids)
    if not documents:
        return Ok("No documents found to delete.")

    document_chunk_ids = get_document_chunk_ids(documents)
    if not await DocumentChunk.load_bulk_ignore_missing(document_chunk_ids):
        return Err("Unable to locate indexed documents.")

    await asyncio.gather(
        *[
            Document.delete_bulk(document_ids),
            DocumentChunk.delete_bulk(document_chunk_ids),
        ]
    )
    return Ok("Documents and associated chunks deleted successfully.")
