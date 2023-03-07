import subprocess

from mindflow.core.diff import run_diff
from mindflow.settings import Settings
from mindflow.utils.prompt_builders import build_context_prompt
from mindflow.utils.prompts import COMMIT_PROMPT_PREFIX


def run_commit() -> str:
    """
    Commit command.
    """
    settings = Settings()

    # Execute the git diff command and retrieve the output as a string
    diff_output = run_diff(("--cached",))

    if diff_output == "No staged changes.":
        return diff_output
    
    response: str = settings.mindflow_models.query.model(
        build_context_prompt(COMMIT_PROMPT_PREFIX, diff_output)
    )

    command = ["git", "commit", "-m"] + [response]

    # Execute the git diff command and retrieve the output as a string
    output = subprocess.check_output(command).decode("utf-8")
    return output
