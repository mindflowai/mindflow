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
    def get_completion(prompt: str, model: str = None) -> str:
        """
        Get response from OpenAI API
        """
        if model is None:
            return prompt[:100]

        return openai.Completion.create(engine=model, prompt=prompt, temperature=0,)[
            "choices"
        ][0]["text"]

    @staticmethod
    def get_embedding(text: str, model: str = None) -> np.ndarray:
        """
        Get embedding from OpenAI API
        """
        if model is None:
            return text[:100]

        return openai.Embedding.create(engine=model, input=text,)["data"][
            0
        ]["embedding"]
