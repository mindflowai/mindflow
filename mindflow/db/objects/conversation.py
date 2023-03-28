from typing import List, Tuple
from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.db.database import Collection

from mindflow.db.objects.base import BaseObject


class Conversation(BaseObject):
    """
    Converstation
    """

    id: str

    # (Role, Message)
    messages: List[Tuple[str, str]]
    total_tokens: int

    _collection = Collection.CONVERSATION
    _database = DATABASE_CONTROLLER.databases.json
