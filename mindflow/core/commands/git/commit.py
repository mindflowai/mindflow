from typing import Tuple, Optional, Union

from mindflow.core.commands.git.diff import run_diff
from mindflow.core.settings import Settings
from mindflow.core.errors import ModelError
from mindflow.core.execute import execute_command_and_print_without_trace
from mindflow.core.text_processing.xml import get_text_within_xml
from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
)
from mindflow.core.prompts import COMMIT_PROMPT_PREFIX

COAUTH_MSG = "Co-authored-by: MindFlow <mf@mindflo.ai>"


def run_commit(
    args: Tuple[str], message_overwrite: Optional[str] = None
) -> Optional[str]:
    settings = Settings()
    query_model = settings.mindflow_models.query.model

    if message_overwrite is None:
        if (diff_output := run_diff(("--cached",))) is None:
            return "Nothing to commit."

        response: Union[ModelError, str] = query_model(
            build_prompt_from_conversation_messages(
                [
                    create_conversation_message(
                        Role.SYSTEM.value, COMMIT_PROMPT_PREFIX
                    ),
                    create_conversation_message(Role.USER.value, diff_output),
                ],
                query_model,
            )
        )
        if isinstance(response, ModelError):
            return response.commit_message

        return execute_command_and_print_without_trace(
            ["git", "commit", "-m"]
            + [f"{get_text_within_xml(response, 'COMMIT')}: {COAUTH_MSG}"]
            + list(args)
        )

    return execute_command_and_print_without_trace(
        ["git", "commit", "-m"] + [message_overwrite] + list(args)
    )
