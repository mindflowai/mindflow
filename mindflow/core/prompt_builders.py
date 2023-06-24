from enum import Enum
from typing import Dict, Union
from typing import List
from mindflow.core.types.model import ConfiguredModel

import anthropic

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
) -> Union[List[Dict], str]:
    if configured_model.model.service == ServiceID.OPENAI.value:
        return messages

    prompt_parts = []
    for message in messages:
        role = message["role"]
        prompt = message["content"]

        if role == Role.SYSTEM.value:
            prompt_parts.append(anthropic.HUMAN_PROMPT + prompt)
            prompt_parts.append(
                anthropic.AI_PROMPT
                + " Sure! I will respond to all following messages with a response like you have just outlined for me."
            )
        elif role in [Role.USER.value, Role.ASSISTANT.value]:
            prompt_parts.append(
                (
                    anthropic.HUMAN_PROMPT
                    if role == Role.USER.value
                    else anthropic.AI_PROMPT
                )
                + prompt
            )

    return "".join(prompt_parts) + anthropic.AI_PROMPT


def prune_messages_to_fit_context_window(
    messages: List[Dict[str, str]], configured_model: ConfiguredModel
) -> List[Dict[str, str]]:
    # Improvement can be made on the estimation here for Anthropic system messages
    content = ""
    for i in range(0, len(messages)):
        content += f"{messages[i]['role']}\n\n {messages[i]['content']}"
        if (
            get_token_count_of_text_for_model(configured_model.tokenizer, content)
            > configured_model.model.hard_token_limit - MinimumReservedLength.CHAT.value
        ):
            return messages[:i]
    return messages
