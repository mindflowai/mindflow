from typing import List, Dict
from mindflow.core.types.store_traits.json import JsonStore


class Conversation(JsonStore):
    id: str

    # (Role, Message)
    messages: List[Dict[str, str]]
    total_tokens: int
