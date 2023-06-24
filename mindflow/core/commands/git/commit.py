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
        gpt_summarize_diff_result = await create_gpt_summarized_diff(
            settings, diff_output
        )
        if isinstance(gpt_summarize_diff_result, Err):
            return gpt_summarize_diff_result
        commit_context = gpt_summarize_diff_result.value

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
