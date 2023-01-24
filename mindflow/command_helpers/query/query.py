"""
This module contains the logic for generating the prompt for the chatbot.
"""

import sys
import numpy as np

from typing import List, Tuple, Union

from mindflow.index.model import Index, index, read_document
from mindflow.client.openai.gpt import GPT
from mindflow.utils.config import config as Config

from sklearn.metrics.pairwise import cosine_similarity


def query(query: str, documents: List[Index.Document], return_prompt: bool = False):
    """
    This function is used to generate a prompt based on a question or summarization task
    """
    embedding_ranked_hashes: List[str] = rank_by_embedding(query, documents)
    if len(embedding_ranked_hashes) == 0:
        print(
            "No index for requested hashes. Please generate index for passed content."
        )
        sys.exit(1)

    selected_content = select_content(embedding_ranked_hashes)

    prompt = f"{query}\n\n{selected_content}"

    # if return_prompt:
        # return prompt
    completion = GPT.get_completion(prompt, Config.GPT_MODEL_COMPLETION)
    return completion


def select_content(ranked_hashes: List[Tuple[str, float]]) -> str:
    """
    This function is used to select the most relevant content for the prompt.
    """
    selected_content: str = ""
    char_limit: int = Config.CHATGPT_TOKEN_LIMIT * 3
    for ranked_hash, _ in ranked_hashes:
        document: Union[Index.Document, None] = index.get_document_by_hash(
            [ranked_hash]
        )
        if document:
            text = read_document(document[0])
            if len(selected_content + text) > char_limit:
                selected_content += text[: char_limit - len(selected_content)]
                break
            selected_content += text

    return selected_content


def rank_by_embedding(
    query: str, documents: List[Index.Document]
) -> List[Tuple[str, float]]:
    """
    This function is used to select the most relevant content for the prompt.
    """
    prompt_embeddings = np.array(
        GPT.get_embedding(query, Config.GPT_MODEL_EMBEDDING)
    ).reshape(1, -1)

    batch_size: int = 100
    ranked_documents: List[Tuple[str, float]] = [None] * len(documents)

    doc_count = 0
    for i in range(0, len(documents), batch_size):
        batch_documents: List[Index.Document] = documents[i : i + batch_size]

        # Get documents from index that have the embeddings
        batch_documents = index.get_document_by_hash(
            document.hash for document in batch_documents
        )
        if len(batch_documents) == 0:
            continue

        document_embeddings = [document.embedding for document in batch_documents]
        document_embeddings = np.array(document_embeddings).reshape(
            len(document_embeddings), -1
        )

        for j, similarity_score in enumerate(
            cosine_similarity(prompt_embeddings, document_embeddings)[0]
        ):
            ranked_documents[doc_count] = (batch_documents[j].hash, similarity_score)
            doc_count += 1

    ranked_documents = [
        document for document in ranked_documents if document is not None
    ]
    return sorted(ranked_documents, key=lambda x: x[1], reverse=True)
