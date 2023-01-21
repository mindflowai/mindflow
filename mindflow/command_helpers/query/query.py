"""
This module contains the logic for generating the prompt for the chatbot.
"""

import sys
import numpy as np

from typing import List, Tuple

from mindflow.index.model import index as Index, Entry
from mindflow.client.openai.gpt import GPT
from mindflow.utils.config import config as Config

from sklearn.metrics.pairwise import cosine_similarity


def query(query: str, hashes: List[str], return_prompt: bool = False):
    """
    This function is used to generate a prompt based on a question or summarization task
    """
    embedding_ranked_hashes: List[str] = rank_by_embedding(query, hashes)
    if len(embedding_ranked_hashes) == 0:
        print(
            "No index for requested hashes. Please generate index for passed content."
        )
        sys.exit(1)

    selected_content = select_content(embedding_ranked_hashes)

    prompt = f"{query}\n\n{selected_content}"

    if return_prompt:
        return prompt

    return GPT.get_completion(prompt, Config.GPT_MODEL_COMPLETION)


def select_content(ranked_hashes: List[Tuple[str, float]]) -> str:
    """
    This function is used to select the most relevant content for the prompt.
    """
    selected_content: str = ""
    char_limit: int = Config.CHATGPT_TOKEN_LIMIT * 3
    for ranked_hash, _ in ranked_hashes:
        content: Entry = Index.get_entry_by_hash([ranked_hash])
        if content:
            text = content[0].read()
            if len(selected_content + text) > char_limit:
                selected_content += text[: char_limit - len(selected_content)]
                break
            selected_content += text

    return selected_content


def rank_by_embedding(query: str, hashes: List[str]) -> List[Tuple[str, float]]:
    """
    This function is used to select the most relevant content for the prompt.
    """
    prompt_embeddings = np.array(
        GPT.get_embedding(query, Config.GPT_MODEL_EMBEDDING)
    ).reshape(1, -1)

    batch_hashes: List[str]
    batch_index: List[Entry]
    batch_size: int = 100
    ranked_hashes: List[Tuple[str, float]] = []

    for i in range(0, len(hashes), batch_size):
        batch_hashes = hashes[i : i + batch_size]
        batch_index = Index.get_entry_by_hash(batch_hashes)
        if len(batch_index) == 0:
            continue

        index_embeddings = [index.get_embedding() for index in batch_index]
        index_embeddings = np.array(index_embeddings).reshape(len(index_embeddings), -1)

        ## print(index_embeddings)
        for j, similarity_score in enumerate(
            cosine_similarity(prompt_embeddings, index_embeddings)[0]
        ):
            ranked_hashes.append((batch_hashes[j], similarity_score))

    return sorted(ranked_hashes, key=lambda x: x[1], reverse=True)
