from typing import List, Union

from mindflow.core.types.conversation import Conversation
from mindflow.core.types.definitions.conversation import ConversationID
from mindflow.core.settings import Settings
from mindflow.core.errors import ModelError
from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
    prune_messages_to_fit_context_window,
)
from mindflow.core.prompts import DEFAULT_CONVERSATION_SYSTEM_PROMPT
from mindflow.core.token_counting import (
    get_token_count_of_messages_for_model,
    get_token_count_from_document_query_for_model,
)


def run_chat(document_paths: List[str], user_query: str) -> str:
    settings = Settings()
    completion_model = settings.mindflow_models.query.model

    if (conversation := Conversation.load(ConversationID.CHAT_0.value)) is None:
        first_message = create_conversation_message(
            Role.SYSTEM.value, DEFAULT_CONVERSATION_SYSTEM_PROMPT
        )
        conversation = Conversation(
            {"id": ConversationID.CHAT_0.value, "messages": [first_message]}
        )

    tokens, texts = get_token_count_from_document_query_for_model(
        document_paths, user_query, completion_model, return_texts=True
    )
    if tokens > completion_model.hard_token_limit:
        raise NotImplementedError(
            f"{tokens} is too large (for now), max is {completion_model.hard_token_limit}."
        )

    conversation.messages.append(
        create_conversation_message(Role.USER.value, "\n".join(texts))
    )
    conversation.messages = prune_messages_to_fit_context_window(
        conversation.messages, completion_model
    )

    response: Union[ModelError, str] = completion_model(
        build_prompt_from_conversation_messages(conversation.messages, completion_model)
    )
    if isinstance(response, ModelError):
        return response.message

    conversation.messages.append(
        create_conversation_message(Role.ASSISTANT.value, response)
    )
    conversation.total_tokens = get_token_count_of_messages_for_model(
        conversation.messages, completion_model
    )

    conversation.save()
    return response
