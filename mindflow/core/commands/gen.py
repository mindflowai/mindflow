from result import Err, Ok, Result
from mindflow.core.types.conversation import Conversation
from mindflow.core.types.definitions.conversation import ConversationID
from mindflow.core.settings import Settings
from mindflow.core.text_processing.xml import get_text_within_xml

from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
    prune_messages_to_fit_context_window,
)
from mindflow.core.token_counting import get_token_count_of_messages_for_model
from mindflow.core.types.model import ConfiguredTextCompletionModel, ModelApiCallError


async def run_code_generation(
    settings: Settings, output_path: str, prompt: str
) -> Result[str, ModelApiCallError]:
    query_model: ConfiguredTextCompletionModel = settings.mindflow_models.query
    if (conversation := Conversation.load(ConversationID.CODE_GEN_0.value)) is None:
        conversation = Conversation(
            {"id": ConversationID.CODE_GEN_0.value, "messages": [], "total_tokens": 0}
        )

    conversation.messages.append(
        create_conversation_message(
            Role.USER.value,
            f"Generate code for '{output_path}' with the following prompt: '{prompt}'. Do NOT use any special characters or symbols, any additional information must be put in comments. Please put the code within XML tags like <GEN></GEN>.",
        )
    )
    conversation.messages = prune_messages_to_fit_context_window(
        conversation.messages, query_model
    )

    query_model_result: Result[str, ModelApiCallError] = await query_model.call_api(
        build_prompt_from_conversation_messages(conversation.messages, query_model)
    )
    if isinstance(query_model_result, Err):
        return query_model_result

    conversation.total_tokens = get_token_count_of_messages_for_model(
        query_model.tokenizer, conversation.messages
    )

    conversation.save()

    return Ok(get_text_within_xml(query_model_result.value, "GEN"))
