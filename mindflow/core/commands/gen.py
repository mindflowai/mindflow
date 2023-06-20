import os
from typing import Union
import click
from mindflow.core.types.conversation import Conversation
from mindflow.core.types.definitions.conversation import ConversationID
from mindflow.core.settings import Settings
from mindflow.core.errors import ModelError
from mindflow.core.text_processing.xml import get_text_within_xml

from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
    prune_messages_to_fit_context_window,
)
from mindflow.core.token_counting import get_token_count_of_messages_for_model


def run_code_generation(output_path: str, prompt: str) -> str:
    settings = Settings()
    completion_model = settings.mindflow_models.query.model

    if os.path.exists(output_path):
        click.confirm(
            f"The output path '{output_path}' already exists. Do you want to overwrite it?",
            abort=True,
        )
        os.remove(output_path)

    if len((output_path_dir := os.path.dirname(output_path))) > 0:
        os.makedirs(output_path_dir, exist_ok=True)

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
        conversation.messages, completion_model
    )

    response: Union[ModelError, str] = completion_model(
        build_prompt_from_conversation_messages(conversation.messages, completion_model)
    )
    if isinstance(response, ModelError):
        return response.message

    with open(output_path, "w") as f:
        f.write(get_text_within_xml(response, "GEN"))

    conversation.total_tokens = get_token_count_of_messages_for_model(
        conversation.messages, completion_model
    )

    conversation.save()

    return f"Code generation complete. Your code is ready to go at {output_path}!"
