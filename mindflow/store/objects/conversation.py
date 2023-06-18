from typing import List, Dict
from mindflow.store.traits.json import JsonStore


class Conversation(JsonStore):
    id: str

    # (Role, Message)
    messages: List[Dict[str, str]]
    total_tokens: int
