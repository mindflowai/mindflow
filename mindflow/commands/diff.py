"""
`diff` command
"""
import subprocess
from mindflow.state import STATE
from mindflow.client.openai.gpt import GPT

from mindflow.utils.prompts import GIT_DIFF_PROMPT_PREFIX

from mindflow.utils.response import handle_response_text


def diff():
    """
    This function is used to generate a git diff and then use it as a prompt for GPT bot.
    """
    # Run Git diff and get the output with prompt suffix
    command = ["git", "diff"]
    if STATE.arguments.git_diff_args is not None:
        command = command + STATE.arguments.git_diff_args

    # Execute the git diff command and retrieve the output as a string
    diff_result = subprocess.check_output(command).decode("utf-8")

    response: str = GPT.query(GIT_DIFF_PROMPT_PREFIX, diff_result)

    handle_response_text(response)
