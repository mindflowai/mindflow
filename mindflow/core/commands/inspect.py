import json
from typing import List

from result import Err, Ok, Result

from mindflow.core.types.document import (
    Document,
    DocumentChunk,
    get_document_chunk_ids,
)


async def run_inspect(document_ids: List[str]) -> Result[str, str]:
    if not (
        document_chunk_ids := get_document_chunk_ids(
            await Document.load_bulk_ignore_missing(document_ids)
        )
    ):
        return Ok("No documents to inspect")

    document_chunks: List[DocumentChunk] = await DocumentChunk.load_bulk_ignore_missing(
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
        return Ok(inspect_output)
    return Err("Unable to locate indexed documents")
