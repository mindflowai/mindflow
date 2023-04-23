import os
from typing import Union
import click
from mindflow.db.objects.conversation import Conversation
from mindflow.db.objects.static_definition.conversation import ConversationID
from mindflow.settings import Settings
from mindflow.utils.errors import ModelError
from mindflow.utils.helpers import get_text_within_xml

from mindflow.utils.prompt_builders import (
    Role,
    build_prompt,
    create_message,
    prune_messages,
)
from mindflow.utils.token import estimate_tokens_from_messages


CODE_GEN_SYSTEM_PROMPT = "All responses must be valid code for the specified language. Do not use any special characters or symbols, any additional information must be put in comments."


def run_code_generation(output_path: str, prompt: str):
    settings = Settings()
    completion_model = settings.mindflow_models.query.model

    if os.path.exists(output_path):
        click.confirm(
            f"The output path '{output_path}' already exists. Do you want to overwrite it?",
            abort=True,
        )
        os.remove(output_path)

    output_path_dir = os.path.dirname(output_path)
    if len(output_path_dir) > 0:
        os.makedirs(output_path_dir, exist_ok=True)

    conversation = Conversation.load(ConversationID.CODE_GEN_0.value)
    if conversation is None:
        conversation = Conversation(
            {"id": ConversationID.CODE_GEN_0.value, "messages": [], "total_tokens": 0}
        )

    conversation.messages.append(
        create_message(
            Role.USER.value,
            f"Generate code for '{output_path}' with the following prompt: '{prompt}'. Do NOT use any special characters or symbols, any additional information must be put in comments. Please put the code within XML tags like <GEN></GEN>.",
        )
    )
    conversation.messages = prune_messages(conversation.messages, completion_model)

    response: Union[ModelError, str] = completion_model(
        build_prompt(conversation.messages, completion_model)
    )
    if isinstance(response, ModelError):
        return response.message

    response = get_text_within_xml(response, "GEN")

    parse_and_write_file(response, output_path)
    conversation.total_tokens = estimate_tokens_from_messages(
        conversation.messages, completion_model
    )

    conversation.save()

    return f"Code generation complete. Your code is ready to go at {output_path}!"


def parse_and_write_file(response: str, output_path: str):
    # take the response and parse it into a valid file.
    with open(output_path, "w") as f:
        f.write(response)
