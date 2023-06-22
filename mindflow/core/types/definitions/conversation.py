from enum import Enum


class ConversationParameterKey(Enum):
    """
    Document argument enum
    """

    ID: str = "id"
    MESSAGES: str = "messages"
    TOTAL_TOKENS: str = "total_tokens"


class ConversationID(Enum):
    """
    Conversation ID enum
    """

    CHAT_0: str = "chat_0"
    CODE_GEN_0: str = "code_gen_0"
