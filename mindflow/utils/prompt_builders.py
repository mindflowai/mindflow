from typing import Dict
from typing import List

from mindflow.db.objects.static_definition.service import ServiceID
import anthropic


def build_context_prompt(context: str, text: str, service: str) -> List[Dict]:
    if service == ServiceID.OPENAI.value:
        return [
            {"role": "system", "content": context},
            {"role": "user", "content": text},
        ]
    else:
        return [
            {"role": anthropic.HUMAN_PROMPT, "content": context},
            {
                "role": anthropic.AI_PROMPT,
                "content": "Sure! I will respond to all following messages with a response like you have just outlined for me.",

            },
            {"role": anthropic.HUMAN_PROMPT, "content": text},
            {"role": anthropic.AI_PROMPT, "content": ""}
        ]
