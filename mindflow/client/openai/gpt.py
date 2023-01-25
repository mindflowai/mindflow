"""
This file is used to load the chat gpt model.
"""

import openai
import numpy as np

from mindflow.utils.config import config as Config


class GPT:
    """
    Class for interacting with OpenAI GPT models
    """

    @staticmethod
    def authorize():
        """
        Authorize OpenAI API
        """
        openai.api_key = Config.openai_auth()

    @staticmethod
    def get_completion(prompt: str, suffix: str = None, model: str = None) -> str:
        """
        Get response from OpenAI API
        """
        response = openai.Completion.create(engine=model, prompt=prompt, suffix=suffix, temperature=0, max_tokens=500)[
            "choices"
        ][0]["text"]
        return response

    @staticmethod
    def get_embedding(text: str, model: str = None) -> np.ndarray:
        """
        Get embedding from OpenAI API
        """
        return openai.Embedding.create(engine=model, input=text,)["data"][
            0
        ]["embedding"]
