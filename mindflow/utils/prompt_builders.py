from enum import Enum
from typing import Dict, Union
from typing import List
from mindflow.store.objects.model import ConfiguredModel

from mindflow.store.objects.static_definition.service import ServiceID
import anthropic
from mindflow.utils.constants import MinimumReservedLength

from mindflow.utils.token import get_token_count_of_text_for_model


class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


def create_conversation_message(role: str, prompt: str) -> Dict[str, str]:
    return {"role": role, "content": prompt}


def build_prompt_from_conversation_messages(
    messages: List[Dict[str, str]], model: ConfiguredModel
) -> Union[List[Dict], str]:
    if model.service == ServiceID.OPENAI.value:
        return messages
    else:
        full_prompt: str = ""
        for message in messages:
            role = message["role"]
            prompt = message["content"]

            if role == Role.SYSTEM.value:
                full_prompt += anthropic.HUMAN_PROMPT
                full_prompt += prompt
                full_prompt += (
                    anthropic.AI_PROMPT
                    + " Sure! I will respond to all following messages with a response like you have just outlined for me."
                )
            elif role == Role.USER.value:
                full_prompt += anthropic.HUMAN_PROMPT
                full_prompt += prompt
            elif role == Role.ASSISTANT.value:
                full_prompt += anthropic.AI_PROMPT
                full_prompt += prompt

        full_prompt += anthropic.AI_PROMPT

        return full_prompt


def prune_messages_to_fit_context_window(
    messages: List[Dict[str, str]], model: ConfiguredModel
) -> List[Dict[str, str]]:
    # Improvement can be made on the estimation here for Anthropic system messages
    content = ""
    for i in range(0, len(messages)):
        content += f"{messages[i]['role']}\n\n {messages[i]['content']}"
        if (
            get_token_count_of_text_for_model(model, content)
            > model.hard_token_limit - MinimumReservedLength.CHAT.value
        ):
            return messages[:i]
    return messages
