"""
`diff` command
"""
import subprocess
from typing import List, Tuple

from mindflow.db.objects.model import Model
from mindflow.settings import Settings
from mindflow.utils.prompt_builders import build_context_prompt

from mindflow.utils.prompts import GIT_DIFF_PROMPT_PREFIX

import concurrent.futures

from mindflow.utils.response import handle_response_text

def run_diff(args: str):
    """
    This function is used to generate a git diff response by feeding git diff to gpt.
    """
    command = ['git', 'diff'] + list(args)

    settings = Settings()
    completion_model: Model = settings.mindflow_models.query.model

    # Execute the git diff command and retrieve the output as a string
    diff_result = subprocess.check_output(command).decode("utf-8")
    batched_parsed_diff_result = batch_git_diffs(parse_git_diff(diff_result), token_limit=completion_model.hard_token_limit)

    response: str = ""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for batch in batched_parsed_diff_result:
            content = ""
            for (file_name, diff_content) in batch:
                content += f"*{file_name}*\n DIFF CONTENT: {diff_content}\n\n"
            future = executor.submit(completion_model, build_context_prompt(GIT_DIFF_PROMPT_PREFIX, content))
            futures.append(future)

        # Process the results as they become available
        for future in concurrent.futures.as_completed(futures):
            response += future.result()
    
    return response

import re

def parse_git_diff(diff_output: str) -> List[Tuple[str, str]]:
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


def batch_git_diffs(file_diffs: List[Tuple[str, str]], token_limit: int) -> List[List[Tuple[str, str]]]:
    batches = []
    current_batch = []
    current_batch_size = 0
    for (file_name, diff_content) in file_diffs:
        if len(diff_content) > token_limit:
            chunks = [diff_content[i:i + token_limit] for i in range(0, len(diff_content), token_limit)]
            for chunk in chunks:
                if current_batch_size + len(chunk) > token_limit * 2:
                    batches.append(current_batch)
                    current_batch = []
                    current_batch_size = 0
                current_batch.append((file_name, chunk))
                current_batch_size += len(chunk)
        elif current_batch_size + len(diff_content) > token_limit * 2:
            batches.append(current_batch)
            current_batch = [(file_name, diff_content)]
            current_batch_size = len(diff_content)
        else:
            current_batch.append((file_name, diff_content))
            current_batch_size += len(diff_content)
    if current_batch:
        batches.append(current_batch)
    return batches
