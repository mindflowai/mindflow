import subprocess
from mindflow.client.gpt import GPT
from mindflow.commands.diff import generate_git_diff_response
from mindflow.state import STATE
from mindflow.utils.prompts import COMMIT_PROMPT_PREFIX


def commit():
    """
    Commit command.
    """
    response: str = GPT.query(COMMIT_PROMPT_PREFIX, generate_git_diff_response())

    command = ["git", "commit", "-m", response]
    if STATE.arguments.commit_args is not None:
        command = command + STATE.arguments.commit_args

    # Execute the git diff command and retrieve the output as a string
    diff_result = subprocess.check_output(command).decode("utf-8")
    print(diff_result)
