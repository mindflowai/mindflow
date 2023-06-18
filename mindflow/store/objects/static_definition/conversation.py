from mindflow.utils.enum import ExtendedEnum


class ConversationParameterKey(ExtendedEnum):
    """
    Document argument enum
    """

    ID: str = "id"
    MESSAGES: str = "messages"
    TOTAL_TOKENS: str = "total_tokens"


class ConversationID(ExtendedEnum):
    """
    Conversation ID enum
    """

    CHAT_0: str = "chat_0"
    CODE_GEN_0: str = "code_gen_0"
