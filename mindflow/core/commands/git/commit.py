from result import Result, Ok, Err
from mindflow.core.commands.git.diff import create_gpt_summarized_diff

from mindflow.core.settings import Settings
from mindflow.core.text_processing.xml import get_text_within_xml
from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
)
from mindflow.core.token_counting import get_token_count_of_text_for_model
from mindflow.core.prompts import COMMIT_PROMPT_PREFIX
from mindflow.core.types.model import ConfiguredTextCompletionModel, ModelApiCallError

COAUTH_MSG = "Co-authored-by: MindFlow <mf@mindflo.ai>"


async def create_gpt_commit_message(
    settings: Settings,
    diff_output: str,
) -> Result[str, ModelApiCallError]:
    commit_context: str = diff_output
    query_model: ConfiguredTextCompletionModel = settings.mindflow_models.query

    if (
        get_token_count_of_text_for_model(
            query_model.tokenizer, diff_output + COMMIT_PROMPT_PREFIX
        )
        > query_model.model.hard_token_limit
    ):
        summarized_diff = ""
        async for char_stream_chunk in create_gpt_summarized_diff(
            settings, diff_output, True
        ):
            if isinstance(char_stream_chunk, Err):
                return char_stream_chunk
            summarized_diff += char_stream_chunk.value

    response: Result[str, ModelApiCallError] = await query_model.call_api(
        build_prompt_from_conversation_messages(
            [
                create_conversation_message(Role.SYSTEM.value, COMMIT_PROMPT_PREFIX),
                create_conversation_message(Role.USER.value, commit_context),
            ],
            query_model,
        )
    )
    if isinstance(response, Err):
        return response

    return Ok(f"{get_text_within_xml(response.value, 'COMMIT')}: {COAUTH_MSG}")
