"""
`diff` command
"""
import concurrent.futures

from typing import Dict, Optional, Union
from typing import List
from typing import Tuple

from mindflow.db.objects.model import ConfiguredModel
from mindflow.settings import Settings
from mindflow.utils.constants import MinimumReservedLength
from mindflow.utils.errors import ModelError
from mindflow.utils.execute import execute_no_trace
from mindflow.utils.prompt_builders import build_context_prompt
from mindflow.utils.prompts import GIT_DIFF_PROMPT_PREFIX

from mindflow.utils.diff_parser import parse_git_diff
from mindflow.utils.token import get_token_count
from tqdm import tqdm


def run_diff(args: Tuple[str], detailed: bool = True) -> Optional[str]:
    """
    This function is used to generate a git diff response by feeding git diff to gpt.
    """
    command = ["git", "diff"] + list(args)

    settings = Settings()
    completion_model: ConfiguredModel = settings.mindflow_models.query.model

    # Execute the git diff command and retrieve the output as a string
    diff_result = execute_no_trace(command)
    if diff_result.strip() == "":
        return None

    diff_dict, excluded_filenames = parse_git_diff(diff_result)
    if len(diff_dict) <= 0:
        return None

    batched_parsed_diff_result = batch_git_diffs(diff_dict, completion_model)

    diff_summary: str = ""
    if len(batched_parsed_diff_result) == 1:
        content = ""
        for file_name, diff_content in batched_parsed_diff_result[0]:
            content += f"*{file_name}*\n DIFF CONTENT: {diff_content}\n\n"
        diff_response: Union[ModelError, str] = completion_model(
            build_context_prompt(GIT_DIFF_PROMPT_PREFIX, content)
        )
        if isinstance(diff_response, ModelError):
            return diff_response.diff_message
        diff_summary += diff_response
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for batch in batched_parsed_diff_result:
                content = ""
                for file_name, diff_content in batch:
                    content += f"*{file_name}*\n DIFF CONTENT: {diff_content}\n\n"
                future: concurrent.futures.Future = executor.submit(
                    completion_model,
                    build_context_prompt(GIT_DIFF_PROMPT_PREFIX, content),
                )
                futures.append(future)

            # Process the results as they become available
            for future in tqdm(concurrent.futures.as_completed(futures)):
                diff_partial_response: Union[ModelError, str] = future.result()
                if isinstance(diff_partial_response, ModelError):
                    return diff_partial_response.diff_partial_message

                diff_summary += diff_partial_response

    if len(excluded_filenames) > 0:
        diff_summary += f"\n\nNOTE: The following files were excluded from the diff: {', '.join(excluded_filenames)}"

    if detailed:
        return diff_summary

    GIT_DIFF_SUMMARIZE_PROMPT = 'What is the higher level purpose of these changes? Keep it short and sweet, don\'t provide any useless or redudant information like "made changes to the code". Do NOT speak in generalities, be specific.'
    summarized = completion_model(
        build_context_prompt(GIT_DIFF_SUMMARIZE_PROMPT, diff_summary)
    )
    return summarized


import re


def batch_git_diffs(
    file_diffs: Dict[str, str], model: ConfiguredModel
) -> List[List[Tuple[str, str]]]:
    batches = []
    current_batch: List = []
    current_batch_text = ""
    for file_name, diff_content in file_diffs.items():
        if (
            get_token_count(model, diff_content)
            > model.hard_token_limit - MinimumReservedLength.DIFF.value
        ):
            ## Split the diff into chunks that are less than the token limit
            chunks = [diff_content]
            while True:
                new_chunks = []
                for chunk in chunks:
                    if (
                        get_token_count(model, chunk)
                        > model.hard_token_limit - MinimumReservedLength.DIFF.value
                    ):
                        half_len = len(chunk) // 2
                        left_half = chunk[:half_len]
                        right_half = chunk[half_len:]
                        new_chunks.extend([left_half, right_half])
                    else:
                        new_chunks.append(chunk)
                if new_chunks == chunks:
                    break
                chunks = new_chunks

            ## Add the chunks to the batch or multiple batches
            for chunk in chunks:
                if (
                    get_token_count(model, current_batch_text + chunk)
                    > model.hard_token_limit - MinimumReservedLength.DIFF.value
                ):
                    batches.append(current_batch)
                    current_batch = []
                    current_batch_text = ""
                current_batch.append((file_name, chunk))
                current_batch_text += chunk

        elif (
            get_token_count(model, current_batch_text + diff_content)
            > model.hard_token_limit - MinimumReservedLength.DIFF.value
        ):
            batches.append(current_batch)
            current_batch = [(file_name, diff_content)]
            current_batch_text = diff_content
        else:
            current_batch.append((file_name, diff_content))
            current_batch_text += diff_content
    if current_batch:
        batches.append(current_batch)
    return batches
