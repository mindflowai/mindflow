"""
This module contains the logic for generating the prompt for the chatbot.
"""

from collections import deque
import sys
import numpy as np

from typing import List, Tuple, Union

from mindflow.index.model import Index, index, read_document
from mindflow.client.openai.gpt import GPT
from mindflow.utils.config import config as Config

from sklearn.metrics.pairwise import cosine_similarity


class DocumentChunk:
    """
    This class is used to store the chunks of a document.
    """

    def __init__(self, path: str, start: int, end: int, embedding: np.ndarray = None):
        self.path = path
        self.start = start
        self.end = end
        self.embedding = embedding

    @classmethod
    def split_document_w_embedding(cls, document = Index.Document) -> List["DocumentChunk"]:
        """
        This function is used to split the document into chunks.
        """
        stack = [document.search_tree]
        chunks: List[DocumentChunk] = []
        while stack:
            node = stack.pop()
            if node["leaves"]:
                for leaf in node["leaves"]:
                    stack.append(leaf)
                    chunks.append(cls(document.path, leaf["start"], leaf["end"], leaf["embedding"]))
        return chunks

def query(query: str, documents: List[Index.Document], return_prompt: bool = False):
    """
    This function is used to generate a prompt based on a question or summarization task
    """
    document_hashes: List[str] = [document.hash for document in documents]
    embedding_ranked_document_chunks: List[Tuple(DocumentChunk, float)] = rank_document_chunks_by_embedding(query, document_hashes)
    if len(embedding_ranked_document_chunks) == 0:
        print(
            "No index for requested hashes. Please generate index for passed content."
        )
        sys.exit(1)

    selected_content = select_content(embedding_ranked_document_chunks)

    if return_prompt:
        return f"{query}\n\n{selected_content}"
        
    return GPT.get_completion(query, selected_content, Config.GPT_MODEL_COMPLETION)


def select_content(ranked_document_chunks: List[DocumentChunk]) -> str:
    """
    This function is used to select the most relevant content for the prompt.
    """
    selected_content: str = ""
    char_limit: int = Config.CHATGPT_TOKEN_LIMIT * 3
    for document_chunk, _ in ranked_document_chunks:
        if document_chunk:
            with open(document_chunk.path, "r") as f:
                f.seek(document_chunk.start)
                text = f.read(document_chunk.end - document_chunk.start)

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
        GPT.get_embedding(query, Config.GPT_MODEL_EMBEDDING)
    ).reshape(1, -1)

    batch_size: int = 100
    ranked_document_chunks: List[Tuple[Tuple(str, int), float]] = [None] * len(documents_hashes)

    doc_count = 0
    for i in range(0, len(ranked_document_chunks), batch_size):
        batch_documents: List[Index.Document] = ranked_document_chunks[i : i + batch_size]

        # Get documents from index that have the embeddings
        batch_documents = index.get_document_by_hash(documents_hashes)
        if len(batch_documents) == 0:
            continue
        
        batch_document_chunks: List[DocumentChunk] = []
        for document in batch_documents:
            batch_document_chunks.extend(DocumentChunk.split_document_w_embedding(document))

        
        document_chunk_embeddings = [document_chunk.embedding for document_chunk in batch_document_chunks]
        for document_chunk in batch_document_chunks:
            document_chunk.embedding = None
        
        document_chunk_embeddings = np.array(document_chunk_embeddings).reshape(
            len(document_chunk_embeddings), -1
            )
        
        for j, similarity_score in enumerate(
            cosine_similarity(prompt_embeddings, document_chunk_embeddings)[0]
        ):
            ranked_document_chunks[doc_count] = (batch_document_chunks[j], similarity_score)
            doc_count += 1

    ranked_document_chunks = [
        ranked_document_chunk for ranked_document_chunk in ranked_document_chunks if ranked_document_chunk is not None
    ]
    return sorted(ranked_document_chunks, key=lambda x: x[1], reverse=True)
