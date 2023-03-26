"""
`query` command
"""
import sys

from typing import Dict, Optional, Union
from typing import List
from typing import Tuple

import numpy as np

from mindflow.db.objects.document import Document, DocumentChunk, get_document_id
from mindflow.db.objects.model import ConfiguredModel
from mindflow.resolving.resolve import resolve_all
from mindflow.settings import Settings
from mindflow.utils.constants import MinimumReservedLength
from mindflow.utils.errors import ModelError
from mindflow.utils.token import get_token_count


def run_query(document_paths: List[str], query: str):
    """
    This function is used to ask a custom question about files, folders, and websites.
    """
    settings = Settings()
    completion_model = settings.mindflow_models.query.model
    embedding_model = settings.mindflow_models.embedding.model

    query_embedding = np.array(embedding_model(query)).reshape(1, -1)

    resolved: Tuple[str, str] = resolve_all(document_paths)
    document_hash_to_path: Dict[str, str] = {
        get_document_id(document_path, document_type): document_path
        for document_path, document_type in resolved
    }
    documents: List[Document] = [
        document
        for document in Document.load_bulk(list(document_hash_to_path.keys()))
        if document is not None
    ]
    total_chunks = sum([document.num_chunks + 1 for document in documents])

    document_chunk_ids = [None] * int(total_chunks)
    j = 0
    for document in documents:
        for i in range(0, int(document.num_chunks) + 1):
            document_chunk_ids[j] = f"{document.id}_{i}"
            j += 1

    top_document_chunks: List[DocumentChunk] = DocumentChunk.query(
        vector=query_embedding, ids=document_chunk_ids
    )
    path_top_document_chunks: List[Tuple[str, List[DocumentChunk]]] = []
    for document_chunk in top_document_chunks:
        document_hash = document_chunk.id.split("_")[0]
        path_top_document_chunks.append(
            (document_hash_to_path[document_hash], document_chunk)
        )

    if len(top_document_chunks) == 0:
        print(
            "No index for requested hashes. Please generate index for passed content."
        )
        sys.exit(1)

    selected_content: str = select_content(
        query, path_top_document_chunks, completion_model
    )
    messages = build_query_messages(
        query,
        selected_content,
    )
    response: Union[ModelError, str] = completion_model(messages)
    if isinstance(response, ModelError):
        return response.query_message

    return response


def build_query_messages(query: str, content: str) -> List[Dict]:
    """
    This function is used to build the query messages for the prompt.
    """
    return [
        {
            "role": "system",
            "content": "You are a helpful virtual assistant responding to a users query using your general knowledge and the text provided below.",
        },
        {"role": "user", "content": query},
        {"role": "system", "content": content},
    ]


def select_content(
    query: str,
    top_document_chunks: List[Tuple[str, DocumentChunk]],
    completion_model: ConfiguredModel,
) -> str:
    """
    This function is used to generate a prompt based on a question or summarization task
    """

    selected_content: str = ""

    for path, document_chunk in top_document_chunks:
        with open(path, "r", encoding="utf-8") as file:
            file.seek(document_chunk.start_pos)
            text = file.read(
                int(document_chunk.end_pos) - int(document_chunk.start_pos)
            )

            selected_content += formated_chunk(path, document_chunk, text)

            if (
                get_token_count(completion_model, query + selected_content)
                > completion_model.hard_token_limit
            ):
                break

    # Perform a binary search to trim the selected content to fit within the token limit
    left, right = 0, len(selected_content)
    while left <= right:
        mid = (left + right) // 2
        if (
            get_token_count(completion_model, query + selected_content[:mid])
            <= completion_model.hard_token_limit - MinimumReservedLength.QUERY.value
        ):
            left = mid + 1
        else:
            right = mid - 1

    # Trim the selected content to the new bounds
    selected_content = selected_content[:right]

    return selected_content


def formated_chunk(path: str, document_chunk: DocumentChunk, text: str) -> str:
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
