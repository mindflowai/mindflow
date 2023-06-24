import asyncio
import os

from typing import Dict, List, Tuple
from result import Ok, Result, Err

from mindflow.core.types.model import (
    ConfiguredModel,
    ConfiguredTextCompletionModel,
    ModelApiCallError,
)
from mindflow.core.settings import Settings
from mindflow.core.constants import MinimumReservedLength

from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
)

from mindflow.core.prompts import GIT_DIFF_PROMPT_PREFIX, GIT_DIFF_SUMMARIZE_PROMPT
from mindflow.core.token_counting import get_token_count_of_text_for_model


async def create_gpt_summarized_diff(
    settings: Settings,
    diff_output: str,
    detailed: bool = False,  # True
) -> Result[str, ModelApiCallError]:
    """Execute git diff and summarize with GPT."""
    index_model: ConfiguredTextCompletionModel = settings.mindflow_models.index

    diff_dict, excluded_filenames = parse_git_diff(diff_output)
    batched_parsed_diff_result = batch_git_diffs(diff_dict, index_model)

    diff_summary: str = ""
    tasks: List[asyncio.Task[Result[str, ModelApiCallError]]] = []
    for batch in batched_parsed_diff_result:
        content = ""
        for file_name, diff_content in batch:
            content += f"*{file_name}*\n DIFF CONTENT: {diff_content}\n\n"

        prompt = build_prompt_from_conversation_messages(
            [
                create_conversation_message(Role.SYSTEM.value, GIT_DIFF_PROMPT_PREFIX),
                create_conversation_message(Role.USER.value, content),
            ],
            index_model,
        )
        tasks.append(asyncio.create_task(index_model.call_api(prompt)))

    results: List[Result[str, ModelApiCallError]] = await asyncio.gather(*tasks)
    for result in results:
        if isinstance(result, Err):
            return result
        diff_summary += result.value

    if len(excluded_filenames) > 0:
        diff_summary += f"\n\nNOTE: The following files were excluded from the diff: {', '.join(excluded_filenames)}"

    if detailed:
        return Ok(diff_summary)

    query_model: ConfiguredTextCompletionModel = settings.mindflow_models.query
    return await query_model.call_api(
        build_prompt_from_conversation_messages(
            [
                create_conversation_message(
                    Role.SYSTEM.value, GIT_DIFF_SUMMARIZE_PROMPT
                ),
                create_conversation_message(Role.USER.value, diff_summary),
            ],
            query_model,
        )
    )


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

    assert len(diffs) > 0
    return diffs, excluded_files


def batch_git_diffs(
    file_diffs: Dict[str, str], configured_model: ConfiguredModel
) -> List[List[Tuple[str, str]]]:
    batches = []
    current_batch: List = []
    current_batch_text = ""
    for file_name, diff_content in file_diffs.items():
        if (
            get_token_count_of_text_for_model(configured_model.tokenizer, diff_content)
            > configured_model.model.hard_token_limit - MinimumReservedLength.DIFF.value
        ):
            chunks = [diff_content]
            while True:
                new_chunks = []
                for chunk in chunks:
                    if (
                        get_token_count_of_text_for_model(
                            configured_model.tokenizer, chunk
                        )
                        > configured_model.model.hard_token_limit
                        - MinimumReservedLength.DIFF.value
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
                    get_token_count_of_text_for_model(
                        configured_model.tokenizer, current_batch_text + chunk
                    )
                    > configured_model.model.hard_token_limit
                    - MinimumReservedLength.DIFF.value
                ):
                    batches.append(current_batch)
                    current_batch = []
                    current_batch_text = ""
                current_batch.append((file_name, chunk))
                current_batch_text += chunk

        elif (
            get_token_count_of_text_for_model(
                configured_model.tokenizer, current_batch_text + diff_content
            )
            > configured_model.model.hard_token_limit - MinimumReservedLength.DIFF.value
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
