import concurrent.futures
import os

from typing import Dict, Optional, Union
from typing import List
from typing import Tuple

from mindflow.core.types.model import ConfiguredModel
from mindflow.core.settings import Settings
from mindflow.core.constants import MinimumReservedLength
from mindflow.core.errors import ModelError
from mindflow.core.execute import execute_command_and_print_without_trace
from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
)
from mindflow.core.prompts import GIT_DIFF_PROMPT_PREFIX, GIT_DIFF_SUMMARIZE_PROMPT

from mindflow.core.token_counting import get_token_count_of_text_for_model
from tqdm import tqdm


def run_diff(args: Tuple[str], detailed: bool = True) -> Optional[str]:
    """Execute git diff and summarize with GPT."""
    settings = Settings()
    completion_model: ConfiguredModel = settings.mindflow_models.query.model

    diff_result = execute_command_and_print_without_trace(
        ["git", "diff"] + list(args)
    ).strip()
    if not diff_result:
        return None

    diff_dict, excluded_filenames = parse_git_diff(diff_result)
    if not diff_dict:
        return None

    batched_parsed_diff_result = batch_git_diffs(diff_dict, completion_model)

    diff_summary: str = ""
    if len(batched_parsed_diff_result) == 1:
        content = ""
        for file_name, diff_content in batched_parsed_diff_result[0]:
            content += f"*{file_name}*\n DIFF CONTENT: {diff_content}\n\n"
        diff_response: Union[ModelError, str] = completion_model(
            build_prompt_from_conversation_messages(
                [
                    create_conversation_message(
                        Role.SYSTEM.value, GIT_DIFF_PROMPT_PREFIX
                    ),
                    create_conversation_message(Role.USER.value, content),
                ],
                completion_model,
            )
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
                    build_prompt_from_conversation_messages(
                        [
                            create_conversation_message(
                                Role.SYSTEM.value, GIT_DIFF_PROMPT_PREFIX
                            ),
                            create_conversation_message(Role.USER.value, content),
                        ],
                        completion_model,
                    ),
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

    summarized = completion_model(
        build_prompt_from_conversation_messages(
            [
                create_conversation_message(
                    Role.SYSTEM.value, GIT_DIFF_SUMMARIZE_PROMPT
                ),
                create_conversation_message(Role.USER.value, content),
            ],
            completion_model,
        )
    )
    return summarized


# NOTE: make sure to have a the "." in the file extension (if applicable)
# NOTE: these are things that WON'T already be git ignored.
IGNORE_FILE_EXTENSIONS = [
    ".pyc",
    ".ipynb",
    ".ipynb_checkpoints",
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".gif",
    ".mp4",
    ".mp3",
    ".mov",
    ".wav",
    ".avi",
    ".zip",
    ".tar",
    ".gzip",
    ".pth",
    ".pt",
    ".exe",
    ".jar",
    ".csv",  # maybe not?
    ".bmp",
    ".emg",
]


def parse_git_diff(diff_str: str):
    diffs = {}
    current_file = None
    current_diff = []  # type: ignore

    excluded_files = []

    for line in diff_str.splitlines(keepends=True):
        if line.startswith("diff --git"):
            # Starting a new file
            if current_file:
                # Add the previous diff to the dictionary
                diffs[current_file] = "".join(current_diff)

            current_file = line.split()[-1]
            current_ext = os.path.splitext(current_file)[1]

            if current_ext in IGNORE_FILE_EXTENSIONS:
                excluded_files.append(current_file)

                # Ignore this file
                current_file = None
                current_diff = []
                continue

            current_diff = [line]
        else:
            # skip lines if we are ignoring this file (TODO - this is a bit hacky)
            if current_file:
                current_diff.append(line)

    # Add the last diff to the dictionary
    if current_file:
        diffs[current_file] = "".join(current_diff)

    return diffs, excluded_files


def batch_git_diffs(
    file_diffs: Dict[str, str], model: ConfiguredModel
) -> List[List[Tuple[str, str]]]:
    batches = []
    current_batch: List = []
    current_batch_text = ""
    for file_name, diff_content in file_diffs.items():
        if (
            get_token_count_of_text_for_model(model, diff_content)
            > model.hard_token_limit - MinimumReservedLength.DIFF.value
        ):
            chunks = [diff_content]
            while True:
                new_chunks = []
                for chunk in chunks:
                    if (
                        get_token_count_of_text_for_model(model, chunk)
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

            for chunk in chunks:
                if (
                    get_token_count_of_text_for_model(model, current_batch_text + chunk)
                    > model.hard_token_limit - MinimumReservedLength.DIFF.value
                ):
                    batches.append(current_batch)
                    current_batch = []
                    current_batch_text = ""
                current_batch.append((file_name, chunk))
                current_batch_text += chunk

        elif (
            get_token_count_of_text_for_model(model, current_batch_text + diff_content)
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
