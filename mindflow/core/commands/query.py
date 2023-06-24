import asyncio
from typing import Dict, List, Tuple
from result import Err, Ok, Result

import numpy as np

from mindflow.core.types.document import (
    Document,
    DocumentChunk,
    get_document_chunk_ids,
    get_document_id,
)
from mindflow.core.resolving.resolve import resolve_paths_to_document_references
from mindflow.core.settings import Settings
from mindflow.core.constants import MinimumReservedLength
from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
)
from mindflow.core.prompts import QUERY_PROMPT_PREFIX
from mindflow.core.token_counting import get_token_count_of_text_for_model
from mindflow.core.types.model import (
    ConfiguredModel,
    ConfiguredTextCompletionModel,
    ConfiguredEmbeddingModel,
    ModelApiCallError,
)


async def run_query(
    settings: Settings, document_paths: List[str], query: str
) -> Result[str, ModelApiCallError]:
    """Query files, folders, and websites."""
    completion_model: ConfiguredTextCompletionModel = settings.mindflow_models.query
    embedding_model: ConfiguredEmbeddingModel = settings.mindflow_models.embedding

    document_hash_to_path: Dict[str, str] = {
        document_id: doc_reference.path
        for doc_reference in resolve_paths_to_document_references(document_paths)
        if (
            document_id := get_document_id(
                doc_reference.path, doc_reference.document_type
            )
        )
        is not None
    }

    # Create two tasks, one for loading the documents and one for loading the query embedding
    document_task = Document.load_bulk_ignore_missing(
        list(document_hash_to_path.keys())
    )
    query_embedding_task = embedding_model.call_api(query)

    # Now await both tasks at the same time
    documents, query_embedding_result = await asyncio.gather(
        document_task, query_embedding_task
    )

    if isinstance(query_embedding_result, Err):
        return query_embedding_result

    document_chunk_ids: List[str] = get_document_chunk_ids(documents)
    if not (
        top_document_chunks := await DocumentChunk.query(
            vector=np.array(query_embedding_result.value).reshape(1, -1),
            ids=document_chunk_ids,
            top_k=100,
        )
    ):
        return Ok(
            "No index for requested hashes. Please generate index for passed content."
        )

    document_selection_batch: List[Tuple[str, DocumentChunk]] = [
        (document_hash_to_path[document_chunk.id.split("_")[0]], document_chunk)
        for document_chunk in top_document_chunks
    ]

    trimmed_content: str = select_and_trim_text_to_fit_context_window(
        completion_model, query, document_selection_batch
    )
    return await completion_model.call_api(
        build_prompt_from_conversation_messages(
            [
                create_conversation_message(Role.SYSTEM.value, QUERY_PROMPT_PREFIX),
                create_conversation_message(
                    Role.USER.value, f"{query}\n\n{trimmed_content}"
                ),
            ],
            completion_model,
        )
    )


def select_and_trim_text_to_fit_context_window(
    configured_model: ConfiguredModel,
    query: str,
    top_document_chunks: List[Tuple[str, DocumentChunk]],
) -> str:
    selected_content: str = ""
    for path, document_chunk in top_document_chunks:
        with open(path, "r", encoding="utf-8") as file:
            file.seek(document_chunk.start_pos)
            selected_content += formatted_chunk(
                path,
                document_chunk,
                file.read(int(document_chunk.end_pos) - int(document_chunk.start_pos)),
            )
            if (
                get_token_count_of_text_for_model(
                    configured_model.tokenizer, query + selected_content
                )
                > configured_model.model.hard_token_limit
            ):
                break

    left, right = 0, len(selected_content)
    while left <= right:
        mid = (left + right) // 2
        if (
            get_token_count_of_text_for_model(
                configured_model.tokenizer, query + selected_content[:mid]
            )
            <= configured_model.model.hard_token_limit
            - MinimumReservedLength.QUERY.value
        ):
            left = mid + 1
            continue
        right = mid - 1

    return selected_content[:right]


def formatted_chunk(path: str, document_chunk: DocumentChunk, text: str) -> str:
    return (
        "Path: "
        + path
        + " Start: "
        + str(document_chunk.start_pos)
        + " End: "
        + str(document_chunk.end_pos)
        + " Text: "
        + text
        + "\n\n"
    )
