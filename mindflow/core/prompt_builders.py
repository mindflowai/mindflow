import json
import anthropic  # type: ignore

from enum import Enum
from typing import Dict, Union, List

from mindflow.core.types.model import ConfiguredModel
from mindflow.core.types.definitions.service import ServiceID
from mindflow.core.constants import MinimumReservedLength
from mindflow.core.token_counting import get_token_count_of_text_for_model


class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


def create_conversation_message(role: str, prompt: str) -> Dict[str, str]:
    return {"role": role, "content": prompt}


def build_prompt_from_conversation_messages(
    messages: List[Dict[str, str]], configured_model: ConfiguredModel
) -> List[Dict]:
    return messages

    # prompt_parts = []
    # for message in messages:
    #     role = message["role"]
    #     prompt = message["content"]

    #     if role == Role.SYSTEM.value:
    #         prompt_parts.append(anthropic.HUMAN_PROMPT + prompt)
    #         prompt_parts.append(
    #             anthropic.AI_PROMPT
    #             + " Sure! I will respond to all following messages with a response like you have just outlined for me."
    #         )
    #     elif role in [Role.USER.value, Role.ASSISTANT.value]:
    #         prompt_parts.append(
    #             (
    #                 anthropic.HUMAN_PROMPT
    #                 if role == Role.USER.value
    #                 else anthropic.AI_PROMPT
    #             )
    #             + prompt
    #         )

    # return "".join(prompt_parts) + anthropic.AI_PROMPT


def prune_messages_to_fit_context_window(
    messages: List[Dict[str, str]], configured_model: ConfiguredModel
) -> List[Dict[str, str]]:
    for i in range(0, len(messages)):
        if (
            get_token_count_of_text_for_model(
                configured_model.tokenizer, json.dumps(messages[i : len(messages)])
            )
            < configured_model.model.hard_token_limit - 1500
        ):
            return messages[i : len(messages)]
    return []
