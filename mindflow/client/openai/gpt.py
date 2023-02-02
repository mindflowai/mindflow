"""
This file is used to load the chat gpt model.
"""

import numpy as np
import openai

from mindflow.state import STATE
from mindflow.utils.prompts import SEARCH_INDEX

if hasattr(STATE.configured_service.openai, "api_key"):
    openai.api_key = STATE.configured_service.openai.api_key


class GPT:
    """
    Class for interacting with OpenAI GPT models
    """

    @staticmethod
    def summarize(text: str) -> str:
        """
        Get response from OpenAI API
        """
        # print(f"Suffix: {suffix}")
        response = openai.Completion.create(
            engine=STATE.configured_model.index.api,
            prompt=f"{SEARCH_INDEX}\n\n{text}",
            temperature=0,
            max_tokens=500,
        )["choices"][0]["text"]

        return response

    @staticmethod
    def query(prompt: str, selected_content: str) -> str:
        """
        Get response from OpenAI API
        """
        # print(f"Suffix: {suffix}")
        response = openai.Completion.create(
            engine=STATE.configured_model.query.api,
            prompt=f"{prompt}\n\n{selected_content}",
            temperature=0,
            max_tokens=500,
        )["choices"][0]["text"]

        return response

    @staticmethod
    def embed(text: str) -> np.ndarray:
        """
        Get embedding from OpenAI API
        """

        return openai.Embedding.create(
            engine=STATE.configured_model.embedding.api, input=text
        )["data"][0]["embedding"]
