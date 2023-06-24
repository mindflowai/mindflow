from typing import List

from result import Err, Result

from mindflow.core.types.conversation import Conversation
from mindflow.core.types.definitions.conversation import ConversationID
from mindflow.core.settings import Settings
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
from mindflow.core.types.model import ConfiguredTextCompletionModel, ModelApiCallError


async def run_chat(
    settings: Settings, document_paths: List[str], user_query: str
) -> Result[str, ModelApiCallError]:
    query_model: ConfiguredTextCompletionModel = settings.mindflow_models.query
    if (conversation := Conversation.load(ConversationID.CHAT_0.value)) is None:
        first_message = create_conversation_message(
            Role.SYSTEM.value, DEFAULT_CONVERSATION_SYSTEM_PROMPT
        )
        conversation = Conversation(
            {"id": ConversationID.CHAT_0.value, "messages": [first_message]}
        )

    tokens, texts = get_token_count_from_document_query_for_model(
        query_model.tokenizer, document_paths, user_query, return_texts=True
    )
    if tokens > query_model.model.hard_token_limit:
        raise NotImplementedError(
            f"{tokens} is too large (for now), max is {query_model.model.hard_token_limit}."
        )

    conversation.messages.append(
        create_conversation_message(Role.USER.value, "\n".join(texts))
    )
    conversation.messages = prune_messages_to_fit_context_window(
        conversation.messages, query_model
    )

    query_model_result: Result[str, ModelApiCallError] = await query_model.call_api(
        build_prompt_from_conversation_messages(conversation.messages, query_model)
    )
    if isinstance(query_model_result, Err):
        return query_model_result

    conversation.messages.append(
        create_conversation_message(Role.ASSISTANT.value, query_model_result.value)
    )
    conversation.total_tokens = get_token_count_of_messages_for_model(
        query_model.tokenizer, conversation.messages
    )

    conversation.save()
    return query_model_result
