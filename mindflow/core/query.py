"""
`query` command
"""
import sys
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Union
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

from mindflow.db.objects.document import Document
from mindflow.db.objects.document import DocumentReference
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

    document_references: List[DocumentReference] = resolve_all(document_paths)
    messages = build_query_messages(
        query,
        select_content(
            query,
            document_references,
            completion_model,
            embedding_model,
        ),
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
    document_references: List[DocumentReference],
    completion_model: ConfiguredModel,
    embedding_model: ConfiguredModel,
) -> str:
    """
    This function is used to generate a prompt based on a question or summarization task
    """
    embedding_ranked_document_chunks: List[
        DocumentChunk
    ] = rank_document_chunks_by_embedding(query, document_references, embedding_model)
    if len(embedding_ranked_document_chunks) == 0:
        print(
            "No index for requested hashes. Please generate index for passed content."
        )
        sys.exit(1)

    selected_content = trim_content(
        embedding_ranked_document_chunks, completion_model, query
    )

    return selected_content


class DocumentChunk:
    """
    This class is used to store the chunks of a document.
    """

    def __init__(
        self, path: str, start: int, end: int, embedding: Optional[np.ndarray] = None
    ):
        self.path = path
        self.start = start
        self.end = end
        self.embedding = embedding

    @classmethod
    def from_search_tree(
        cls,
        document: Document,
        embedding_model: ConfiguredModel,
    ) -> Tuple[List["DocumentChunk"], List[np.ndarray]]:
        """
        This function is used to split the document into chunks.
        """

        stack = [document.search_tree]
        chunks: List["DocumentChunk"] = [
            cls(
                document.path,
                document.search_tree["start"],
                document.search_tree["end"],
            )
        ]
        embedding_response: Union[ModelError, np.ndarray] = embedding_model(
            document.search_tree["summary"]
        )
        if isinstance(embedding_response, ModelError):
            print(embedding_response.embedding_message)
            return [], []

        embeddings: List[np.ndarray] = [embedding_response]
        rolling_summary: List[str] = []
        while stack:
            node = stack.pop()
            rolling_summary.append(node["summary"])
            if node["leaves"]:
                for leaf in node["leaves"]:
                    stack.append(leaf)
                    chunks.append(cls(document.path, leaf["start"], leaf["end"]))
                    rolling_summary_embedding_response: Union[
                        np.ndarray, ModelError
                    ] = embedding_model(
                        "\n\n".join(rolling_summary) + "\n\n" + leaf["summary"],
                    )
                    if isinstance(rolling_summary_embedding_response, ModelError):
                        print(rolling_summary_embedding_response.embedding_message)
                        continue
                    embeddings.append(rolling_summary_embedding_response)
            rolling_summary.pop()

        return chunks, embeddings


def trim_content(
    ranked_document_chunks: List[DocumentChunk], model: ConfiguredModel, query: str
) -> str:
    """
    This function is used to select the most relevant content for the prompt.
    """
    selected_content: str = ""

    for document_chunk in ranked_document_chunks:
        if document_chunk:
            with open(document_chunk.path, "r", encoding="utf-8") as file:
                file.seek(document_chunk.start)
                text = file.read(document_chunk.end - document_chunk.start)

                # Perform a binary search to find the maximum amount of text that fits within the token limit
                left, right = 0, len(text)
                while left <= right:
                    mid = (left + right) // 2
                    if (
                        get_token_count(model, query + selected_content + text[:mid])
                        <= model.hard_token_limit - MinimumReservedLength.QUERY.value
                    ):
                        left = mid + 1
                    else:
                        right = mid - 1

                # Add the selected text to the selected content
                selected_content += text[:right]
    return selected_content


def rank_document_chunks_by_embedding(
    query: str,
    document_references: List[DocumentReference],
    embedding_model: ConfiguredModel,
) -> List[DocumentChunk]:
    """
    This function is used to select the most relevant content for the prompt.
    """
    prompt_embeddings = np.array(embedding_model(query)).reshape(1, -1)

    ranked_document_chunks = []
    for i in range(0, len(document_references), 100):
        document_ids = [document.id for document in document_references[i : i + 100]]
        documents: List[Optional[Document]] = Document.load_bulk(document_ids)
        filtered_documents: List[Document] = [
            document for document in documents if document is not None
        ]
        if documents == []:
            continue

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [
                executor.submit(
                    DocumentChunk.from_search_tree, document, embedding_model
                )
                for document in filtered_documents
            ]
            for future in as_completed(futures):
                document_chunks, document_chunk_embeddings = future.result()
                similarities = cosine_similarity(
                    prompt_embeddings, document_chunk_embeddings
                )[0]
                ranked_document_chunks.extend(list(zip(document_chunks, similarities)))

    ranked_document_chunks.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, _ in ranked_document_chunks]
