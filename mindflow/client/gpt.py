"""
This file is used to load the chat gpt model.
"""

from typing import Optional
import numpy as np
import openai

from mindflow.state import STATE
from mindflow.utils.prompts import SEARCH_INDEX


class GPTEndpoints:
    """
    Class for interacting with OpenAI GPT models
    """

    @property
    def configured_api(self):
        openai.api_key = STATE.configured_service.openai.api_key
        return openai

    def summarize(self, text: str) -> str:
        """
        Get response from OpenAI API
        """
        try:
            # print(f"Suffix: {suffix}")
            response = self.configured_api.Completion.create(
                engine=STATE.configured_model.index.api,
                prompt=f"{SEARCH_INDEX}\n\n{text}",
                temperature=0,
                max_tokens=500,
            )["choices"][0]["text"]

            return response
        except Exception as e:
            print(e)
            return ""

    def query(self, prompt: str, selected_content: Optional[str] = None) -> str:
        """
        Get response from OpenAI API
        """
        try:
            # print(f"Suffix: {suffix}")
            response = self.configured_api.Completion.create(
                engine=STATE.configured_model.query.api,
                prompt=prompt,
                suffix=selected_content,
                temperature=0,
                max_tokens=500,
            )["choices"][0]["text"]
            return response

        except Exception as e:
            print(e)
            return ""

    def embed(self, text: str) -> np.ndarray:
        """
        Get embedding from OpenAI API
        """
        try:
            response = self.configured_api.Embedding.create(
                engine=STATE.configured_model.embedding.api, input=text
            )["data"][0]["embedding"]

            return response
        except Exception as e:
            print(e)
            return np.array([])


GPT = GPTEndpoints()
