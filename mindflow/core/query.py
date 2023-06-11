"""
`query` command
"""
import sys

from typing import Dict, List, Union, Tuple

import numpy as np

from mindflow.db.objects.document import (
    Document,
    DocumentChunk,
    DocumentReference,
    get_document_chunk_ids,
    get_document_id,
)
from mindflow.db.objects.model import ConfiguredModel
from mindflow.resolving.resolve import resolve_paths_to_document_references
from mindflow.settings import Settings
from mindflow.utils.constants import MinimumReservedLength
from mindflow.utils.errors import ModelError
from mindflow.utils.prompt_builders import (
    Role,
    build_conversation_from_conversation_messages,
    create_conversation_message,
)
from mindflow.utils.prompts import QUERY_PROMPT_PREFIX
from mindflow.utils.token import get_token_count_of_text_for_model


def run_query(document_paths: List[str], query: str):
    """
    This function is used to ask a custom question about files, folders, and websites.
    """
    settings = Settings()
    completion_model = settings.mindflow_models.query.model
    embedding_model = settings.mindflow_models.embedding.model

    document_references: List[DocumentReference] = resolve_paths_to_document_references(
        document_paths
    )
    document_hash_to_path: Dict[str, str] = {}
    for document_reference in document_references:
        document_id = get_document_id(
            document_reference.path, document_reference.document_type
        )
        if document_id is not None:
            document_hash_to_path[document_id] = document_reference.path

    document_chunk_ids = get_document_chunk_ids(
        Document.load_bulk(list(document_hash_to_path.keys()), return_none=False)
    )
    top_document_chunks: List[DocumentChunk] = DocumentChunk.query(
        vector=np.array(embedding_model(query)).reshape(1, -1),
        ids=document_chunk_ids,
        top_k=100,
    )

    document_selection_batch: List[Tuple[str, DocumentChunk]] = [
        (document_hash_to_path[document_chunk.id.split("_")[0]], document_chunk)
        for document_chunk in top_document_chunks
    ]

    if not top_document_chunks:
        print(
            "No index for requested hashes. Please generate index for passed content."
        )
        sys.exit(1)

    trimmed_content: str = select_and_trim_text_to_fit_context_window(
        query, document_selection_batch, completion_model
    )
    response: Union[ModelError, str] = completion_model(
        build_conversation_from_conversation_messages(
            [
                create_conversation_message(Role.SYSTEM.value, QUERY_PROMPT_PREFIX),
                create_conversation_message(
                    Role.USER.value, f"{query}\n\n{trimmed_content}"
                ),
            ],
            completion_model,
        )
    )
    if isinstance(response, ModelError):
        return response.query_message

    return response


def select_and_trim_text_to_fit_context_window(
    query: str,
    top_document_chunks: List[Tuple[str, DocumentChunk]],
    completion_model: ConfiguredModel,
) -> str:
    selected_content: str = ""
    for path, document_chunk in top_document_chunks:
        with open(path, "r", encoding="utf-8") as file:
            file.seek(document_chunk.start_pos)
            text = file.read(
                int(document_chunk.end_pos) - int(document_chunk.start_pos)
            )

            selected_content += formatted_chunk(path, document_chunk, text)

            if (
                get_token_count_of_text_for_model(
                    completion_model, query + selected_content
                )
                > completion_model.hard_token_limit
            ):
                break

    left, right = 0, len(selected_content)
    while left <= right:
        mid = (left + right) // 2
        if (
            get_token_count_of_text_for_model(
                completion_model, query + selected_content[:mid]
            )
            <= completion_model.hard_token_limit - MinimumReservedLength.QUERY.value
        ):
            left = mid + 1
        else:
            right = mid - 1

    selected_content = selected_content[:right]
    return selected_content


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
