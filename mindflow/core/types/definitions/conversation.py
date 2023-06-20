from enum import Enum


class ConversationParameterKey(Enum):
    ID: str = "id"
    MESSAGES: str = "messages"
    TOTAL_TOKENS: str = "total_tokens"


class ConversationID(Enum):
    CHAT_0: str = "chat_0"
    CODE_GEN_0: str = "code_gen_0"
