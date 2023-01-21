import subprocess
from typing import List

from mindflow.utils.prompts import GIT_DIFF_PROMPT_PREFIX


def generate_diff_prompt(diffargs: List[str]) -> str:
    """
    This function is used to generate a prompt based on a diff.
    """
    command = ["git", "diff"] + diffargs

    # Execute the git diff command and retrieve the output as a string
    diff_result = subprocess.check_output(command).decode("utf-8")

    return f"{GIT_DIFF_PROMPT_PREFIX}\n\n{diff_result}"
