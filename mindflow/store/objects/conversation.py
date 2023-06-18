from typing import List, Tuple
from mindflow.store.traits.json import JsonStore


class Conversation(JsonStore):
    id: str

    # (Role, Message)
    messages: List[Tuple[str, str]]
    total_tokens: int
