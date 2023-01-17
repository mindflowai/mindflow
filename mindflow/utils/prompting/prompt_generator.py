"""
This module contains the logic for generating the prompt for the chatbot.
"""
import subprocess
from mindflow.utils.prompting.prompts import GIT_DIFF_PROMPT_PREFIX


def generate_diff_prompt(diffargs: str):
    """
    This function is used to generate a prompt for the chatbot based on the git diff.
    """
    command = ["git", "diff"] + diffargs

    # Execute the git diff command and retrieve the output as a string
    diff_result = subprocess.check_output(command).decode("utf-8")

    return f"{GIT_DIFF_PROMPT_PREFIX}\n\n{diff_result}"
