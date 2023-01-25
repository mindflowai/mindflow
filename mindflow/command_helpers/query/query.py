"""
This module contains the logic for generating the prompt for the chatbot.
"""

from typing import List, Tuple

import sys
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from mindflow.index.model import Index, index
from mindflow.client.openai.gpt import GPT
from mindflow.utils.config import IndexType, config as CONFIG


class DocumentChunk:
    """
    This class is used to store the chunks of a document.
    """

    def __init__(self, path: str, start: int, end: int, embedding: np.ndarray = None):
        self.path = path
        self.start = start
        self.end = end
        self.embedding = embedding

    @staticmethod
    def from_search_tree(
        document: Index.Document,
    ) -> Tuple[List["DocumentChunk"], List[np.array]]:
        """
        This function is used to split the document into chunks.
        """
        if document.index_type == IndexType.DEEP:
            return DocumentChunk._from_search_tree_deep(
                document.search_tree, document.path
            )
        return DocumentChunk._from_search_tree_shallow(
            document.search_tree, document.path
        )

    @classmethod
    def _from_search_tree_deep(
        cls, search_tree: dict, path: str
    ) -> Tuple[List["DocumentChunk"], List[np.array]]:
        """
        This function is used to split the document into chunks.
        """
        stack = [search_tree]
        chunks: List["DocumentChunk"] = [
            cls(path, search_tree["start"], search_tree["end"])
        ]
        embeddings: List[str] = [
            GPT.get_embedding(
                search_tree["summary"],
                CONFIG.GPT_MODEL_EMBEDDING,
            )
        ]
        rolling_summary: List[str] = []
        while stack:
            node = stack.pop()
            rolling_summary.append(node["summary"])
            if node["leaves"]:
                for leaf in node["leaves"]:
                    stack.append(leaf)
                    chunks.append(cls(path, leaf["start"], leaf["end"]))
                    rolling_summary_embedding = GPT.get_embedding(
                        "\n\n".join(rolling_summary) + "\n\n" + leaf["summary"],
                        CONFIG.GPT_MODEL_EMBEDDING,
                    )
                    embeddings.append(rolling_summary_embedding)
            rolling_summary.pop()

        return chunks, embeddings

    @classmethod
    def _from_search_tree_shallow(
        cls, search_tree: dict, path: str
    ) -> Tuple[List["DocumentChunk"], List[np.array]]:
        """
        This function is used to split the document into chunks.
        """
        stack = [search_tree]
        chunks: List["DocumentChunk"] = [
            cls(path, search_tree["start"], search_tree["end"])
        ]
        embeddings: List[np.ndarray] = [search_tree["embedding"]]
        while stack:
            node = stack.pop()
            if node["leaves"]:
                for leaf in node["leaves"]:
                    stack.append(leaf)
                    chunks.append(cls(path, leaf["start"], leaf["end"]))
                    embeddings.append(np.array(leaf["embedding"]))

        return chunks, embeddings


def query(query: str, documents: List[Index.Document], return_prompt: bool = False):
    """
    This function is used to generate a prompt based on a question or summarization task
    """
    document_hashes: List[str] = [document.hash for document in documents]
    embedding_ranked_document_chunks: List[
        Tuple(DocumentChunk, float)
    ] = rank_document_chunks_by_embedding(query, document_hashes)
    if len(embedding_ranked_document_chunks) == 0:
        print(
            "No index for requested hashes. Please generate index for passed content."
        )
        sys.exit(1)

    selected_content = select_content(embedding_ranked_document_chunks)

    if return_prompt:
        return f"{query}\n\n{selected_content}"

    return GPT.get_completion(query, selected_content, CONFIG.GPT_MODEL_COMPLETION)


def select_content(ranked_document_chunks: List[DocumentChunk]) -> str:
    """
    This function is used to select the most relevant content for the prompt.
    """
    selected_content: str = ""
    char_limit: int = CONFIG.CHATGPT_TOKEN_LIMIT * 3
    for document_chunk, _ in ranked_document_chunks:
        if document_chunk:
            with open(document_chunk.path, "r", encoding="utf-8") as file:
                file.seek(document_chunk.start)
                text = file.read(document_chunk.end - document_chunk.start)
                if len(selected_content + text) > char_limit:
                    selected_content += text[: char_limit - len(selected_content)]
                    break
                selected_content += text

    return selected_content


def rank_document_chunks_by_embedding(
    query: str, documents_hashes: List[str]
) -> List[Tuple[DocumentChunk, float]]:
    """
    This function is used to select the most relevant content for the prompt.
    """
    prompt_embeddings = np.array(
        GPT.get_embedding(query, CONFIG.GPT_MODEL_EMBEDDING)
    ).reshape(1, -1)

    ranked_document_chunks = []
    for i in range(0, len(documents_hashes), 100):
        for document in index.get_document_by_hash(documents_hashes[i : i + 100]):
            document_chunks, document_chunk_embeddings = DocumentChunk.from_search_tree(
                document
            )
            similarities = cosine_similarity(
                prompt_embeddings, document_chunk_embeddings
            )[0]
            ranked_document_chunks.extend(list(zip(document_chunks, similarities)))

    ranked_document_chunks.sort(key=lambda x: x[1], reverse=True)
    return ranked_document_chunks
