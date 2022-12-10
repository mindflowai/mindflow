"""
This module contains the logic for generating the prompt for the chatbot.
"""
import json
import subprocess

from mindflow.resolve.resolve import resolve
from mindflow.utils.prompts import GIT_DIFF_PROMPT_PREFIX


def generate_diff_prompt(args):
    """
    This function is used to generate a prompt for the chatbot based on the git diff.
    """
    command = ["git", "diff"] + args.diffargs

    # Execute the git diff command and retrieve the output as a string
    diff_result = subprocess.check_output(command).decode("utf-8")

    return f"{GIT_DIFF_PROMPT_PREFIX}\n\n{diff_result}"


def generate_prompt_from_files(args, question):
    """
    This function is used to generate a prompt based on a question or summarization task
    """
    reference_text_dict = {}
    {reference_text_dict.update(resolve(reference)) for reference in args.references}

    json_str = json.dumps(reference_text_dict, indent=4)

    return f"{question}\n\n{json_str}"
