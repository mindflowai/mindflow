"""
This file is used to load the chat gpt model.
"""

from typing import Optional
import numpy as np
import openai
from mindflow.db.objects.model import Model
from mindflow.db.objects.static_definition.model import ModelID

from mindflow.utils.prompts import SEARCH_INDEX


class GPTEndpoints:
    """
    Class for interacting with OpenAI GPT models
    """

    @property
    def configured_api(self):
        openai.api_key = STATE.settings.services.openai.api_key
        return openai

    def summarize(self, text: str) -> str:
        """
        Get response from OpenAI API
        """
        try:
            # print(f"Suffix: {suffix}")
            if STATE.settings.mindflow_models.index.model.api in [ModelID.GPT_3_5_TURBO.value, ModelID.GPT_3_5_TURBO_0301.value]:
                response = self.configured_api.ChatCompletion.create(
                    model=STATE.settings.mindflow_models.index.model.api,
                    messages=[
                        {"role": "system", "content": SEARCH_INDEX},
                        {"role": "user", "content": text},
                    ],
                    temperature=0,
                    max_tokens=500,
                    stop=["\n\n"],
                )["choices"][0]["message"]["content"]
            else:
                response = self.configured_api.Completion.create(
                    engine=STATE.settings.mindflow_models.index.model.api,
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

            if STATE.settings.mindflow_models.query.model.api in ["gpt-3.5-turbo", "gpt-3.5-turbo-0301"]:
                response = self.configured_api.ChatCompletion.create(
                    model=STATE.settings.mindflow_models.index.model.api,
                    messages=[
                        {"role": "system", "content": "You are a helpful virtual assistant responding to a users query using your general knowledge and the text provided below."},
                        {"role": "user", "content": prompt},
                        {"role": "system", "content": selected_content}
                    ],
                    temperature=0,
                    max_tokens=1000,
                )["choices"][0]["message"]["content"]

                return response
            else:
                response = self.configured_api.Completion.create(
                    engine=STATE.settings.mindflow_models.query.model.api,
                    prompt=prompt,
                    suffix=selected_content,
                    temperature=0,
                    max_tokens=1000,
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
                engine=STATE.settings.mindflow_models.embedding.model.api, input=text
            )["data"][0]["embedding"]

            return response
        except Exception as e:
            print(e)
            return np.array([])


def get_response(configured_api: openai, model: Model, prompt: str, selected_content: Optional[str] = None) -> str:
    response = configured_api.ChatCompletion.create(
                model=model.api,
                messages=[
                    {"role": "system", "content": "You are a helpful virtual assistant responding to a users query using your general knowledge and the text provided below."},
                    {"role": "user", "content": prompt},
                    {"role": "system", "content": selected_content}
                ],
                temperature=0,
                max_tokens=1000,
            )["choices"][0]["message"]["content"]

openai.Model.retrieve()

GPT = GPTEndpoints()
