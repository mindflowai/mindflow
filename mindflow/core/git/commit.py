import subprocess
from typing import Tuple, Optional, Union

from mindflow.core.git.diff import run_diff
from mindflow.settings import Settings
from mindflow.utils.errors import ModelError
from mindflow.utils.prompt_builders import build_context_prompt
from mindflow.utils.prompts import COMMIT_PROMPT_PREFIX


def run_commit(args: Tuple[str], message_overwrite: Optional[str] = None) -> str:
    """
    Commit command.
    """
    settings = Settings()

    if message_overwrite is None:
        # Execute the git diff command and retrieve the output as a string
        diff_output = run_diff(("--cached",))

        if diff_output == "No staged changes.":
            return diff_output

        response: Union[ModelError, str] = settings.mindflow_models.query.model(
            build_context_prompt(COMMIT_PROMPT_PREFIX, diff_output)
        )
        if isinstance(response, ModelError):
            return response.commit_message

        # add co-authorship to commit message
        response += "\n\nCo-authored-by: MindFlow <mf@mindflo.ai>"
    else:
        response = message_overwrite

    command = ["git", "commit", "-m"] + [response] + list(args)

    # Execute the git diff command and retrieve the output as a string
    output = subprocess.check_output(command).decode("utf-8")
    return output
