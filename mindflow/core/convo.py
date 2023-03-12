import json
import os
from typing import List, Union

from mindflow.db.db.json import get_mindflow_dir


DEFAULT_SYSTEM_PROMPT = "You are a senior software engineer responding to another software engineer's chat messages regarding your codebase, make sure to be polite and helpful, and provide thorough answers with example code when necessary."


from mindflow.settings import Settings
from mindflow.utils.token import get_batch_token_count


def get_chat_model():
    settings = Settings()
    completion_model = settings.mindflow_models.query.model
    return completion_model


def estimate_tokens(document_paths: List[str], query: str, return_texts: bool = False):
    texts = [query]
    for document_path in document_paths:
        # check if directory
        if os.path.isdir(document_path):
            raise NotImplementedError("Directory support not yet implemented.")

        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Could not find file at {document_path}")

        file_text = {open(document_path, "r").read()}
        text = f"```{file_text}```"
        texts.append(text)

    tokens = get_batch_token_count(get_chat_model(), texts)
    if return_texts:
        return tokens, texts
    return tokens


class Conversation:
    def __init__(
        self,
        conversation_id: Union[int, str] = 0,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ):
        self.conversation_id = conversation_id
        self.system_prompt = system_prompt
        self.system_prompt_tokens = estimate_tokens([], system_prompt)
        self.chat_model = get_chat_model()

        self.conversation_filename = os.path.join(
            get_mindflow_dir(), f"current_conversation_{self.conversation_id}.json"
        )

        # Load existing conversation from file if it exists
        if os.path.exists(self.conversation_filename):
            with open(self.conversation_filename, "r") as f:
                convo = json.load(f)
                assert len(convo) > 0
                assert convo[0]["role"] == "system"

                convo[0]["content"] = self.system_prompt  # update system prompt
                convo[0][
                    "_tokens"
                ] = self.system_prompt_tokens  # update system prompt tokens

                self.messages = convo
        else:
            self.messages = [
                {
                    "role": "system",
                    "content": system_prompt,
                    "_tokens": self.system_prompt_tokens,
                }
            ]

    @property
    def token_limit(self):
        return self.chat_model.hard_token_limit

    @property
    def total_tokens(self):
        return sum([message["_tokens"] for message in self.messages])

    def add_message(self, content: str, role: str = "user"):
        message = {
            "role": role,
            "content": content,
            "_tokens": estimate_tokens([], content),
        }

        if message["_tokens"] > self.token_limit:
            raise ValueError(
                f"Message exceeds hard token limit of {self.token_limit} tokens!"
            )

        self.messages.append(message)
        self._prune()

    def clear(self):
        system_message = self.messages[0]
        self.messages.clear()
        self.messages.append(system_message)

    def _validate(self):
        # NOTE: we need to make sure we always keep the system prompt (and that there's always only 1)
        if self.messages[0]["role"] != "system":
            raise ValueError()
        for message in self.messages[1:]:
            if message["role"] == "system":
                raise ValueError()

        # make sure the tokens don't sum to more than the hard token limit
        if self.total_tokens > self.token_limit:
            raise ValueError(
                f"Too many tokens! Got {self.total_tokens} tokens, but the hard token limit is {self.token_limit}!"
            )

    def _prune(self):
        # remove earlier messages until we are below the hard token limit

        system_message = self.messages[0]

        reached_limit = False
        tokens_sum = system_message["_tokens"]  # start with the system prompt
        for i, message in enumerate(reversed(self.messages[1:])):
            tokens_sum += message["_tokens"]
            if tokens_sum > self.token_limit:
                reached_limit = True
                break

        if reached_limit:
            keep_messages = self.messages[i + 1 :]
            self.messages.clear()
            self.messages.append(system_message)
            self.messages.extend(keep_messages)

        self._validate()

    def get_prompt(self):
        # don't include the _tokens key
        prompt = []
        for message in self.messages:
            prompt.append({"role": message["role"], "content": message["content"]})
        return prompt

    def get_response(self):
        response = self.chat_model(self.get_prompt())

        if response is None:
            raise ValueError("Response is None!")

        return response

    def save(self):
        self._validate()

        with open(self.conversation_filename, "w") as f:
            json.dump(self.messages, f, indent=2)
