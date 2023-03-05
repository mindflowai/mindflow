"""
`diff` command
"""
import subprocess
from typing import List, Tuple
from mindflow.state import STATE
from mindflow.client.gpt import GPT

from mindflow.utils.prompts import GIT_DIFF_PROMPT_PREFIX

from mindflow.utils.response import handle_response_text


def diff():
    """
    Generate response to a git diff and handle output
    """
    handle_response_text(generate_git_diff_response())

def generate_git_diff_response() -> str:
    """
    This function is used to generate a git diff response by feeding git diff to gpt.
    """
    command = ["git", "diff", '--cached']
    if STATE.arguments.diff_args is not None:
        command = command + STATE.arguments.diff_args

    # Execute the git diff command and retrieve the output as a string
    diff_result = subprocess.check_output(command).decode("utf-8")
    batched_parsed_diff_result = batch_git_diffs(parse_git_diff(diff_result))

    response: str = ""
    for batch in batched_parsed_diff_result:
        content: str = ""
        for (file_name, diff_content) in batch:
            content += f"*{file_name}*\n DIFF CONTENT: {diff_content}\n\n"
        
        response += GPT.query(GIT_DIFF_PROMPT_PREFIX, content)
    
    return response

import re

def parse_git_diff(diff_output) -> List[Tuple[str, str]]:
    file_diffs = []
    current_diff = None
    for line in diff_output.split('\n'):
        if line.startswith('diff --git'):
            if current_diff is not None:
                file_diffs.append(current_diff)
            current_diff = {'file_name': None, 'content': []}
            match = re.match(r'^diff --git a/(.+?) b/.+?$', line)
            if match:
                current_diff['file_name'] = match.group(1)
        if current_diff is not None:
            current_diff['content'].append(line)
    if current_diff is not None:
        file_diffs.append(current_diff)
    return [(diff['file_name'], '\n'.join(diff['content'])) for diff in file_diffs]


def batch_git_diffs(file_diffs: List[Tuple[str, str]]) -> List[List[Tuple[str, str]]]:
    batches = []
    current_batch = []
    current_batch_size = 0
    for (file_name, diff_content) in file_diffs:
        if len(diff_content) > STATE.settings.mindflow_models.query.model.hard_token_limit:
            chunks = [diff_content[i:i + STATE.settings.mindflow_models.query.model.hard_token_limit] for i in range(0, len(diff_content), STATE.settings.mindflow_models.query.model.hard_token_limit)]
            for chunk in chunks:
                if current_batch_size + len(chunk) > STATE.settings.mindflow_models.query.model.hard_token_limit * 2:
                    batches.append(current_batch)
                    current_batch = []
                    current_batch_size = 0
                current_batch.append((file_name, chunk))
                current_batch_size += len(chunk)
        elif current_batch_size + len(diff_content) > STATE.settings.mindflow_models.query.model.hard_token_limit * 2:
            batches.append(current_batch)
            current_batch = [(file_name, diff_content)]
            current_batch_size = len(diff_content)
        else:
            current_batch.append((file_name, diff_content))
            current_batch_size += len(diff_content)
    if current_batch:
        batches.append(current_batch)
    return batches
