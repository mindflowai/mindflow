from typing import Tuple, Optional, Union

from mindflow.core.git.diff import run_diff
from mindflow.settings import Settings
from mindflow.utils.constants import COAUTH_MSG
from mindflow.utils.errors import ModelError
from mindflow.utils.execute import execute_no_trace
from mindflow.utils.helpers import get_text_within_xml
from mindflow.utils.prompt_builders import Role, build_prompt, create_message
from mindflow.utils.prompts import COMMIT_PROMPT_PREFIX


def run_commit(
    args: Tuple[str], message_overwrite: Optional[str] = None
) -> Optional[str]:
    """
    Commit command.
    """
    settings = Settings()
    query_model = settings.mindflow_models.query.model

    if message_overwrite is None:
        # Execute the git diff command and retrieve the output as a string
        diff_output = run_diff(("--cached",))
        if diff_output is None:
            return "Nothing to commit."

        response: Union[ModelError, str] = query_model(
            build_prompt(
                [
                    create_message(Role.SYSTEM.value, COMMIT_PROMPT_PREFIX),
                    create_message(Role.USER.value, diff_output),
                ],
                query_model,
            )
        )
        if isinstance(response, ModelError):
            return response.commit_message

        return execute_no_trace(
            ["git", "commit", "-m"]
            + [f"{get_text_within_xml(response, 'COMMIT')}: {COAUTH_MSG}"]
            + list(args)
        )

    return execute_no_trace(["git", "commit", "-m"] + [message_overwrite] + list(args))
