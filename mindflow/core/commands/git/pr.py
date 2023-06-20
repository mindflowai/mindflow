import concurrent.futures
import subprocess
from typing import Optional, Tuple, Union

from mindflow.core.commands.git.diff import run_diff
from mindflow.core.settings import Settings
from mindflow.core.command_parse import get_flag_values_from_args
from mindflow.core.errors import ModelError
from mindflow.core.execute import execute_command_and_print_without_trace
from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
)
from mindflow.core.prompts import PR_BODY_PREFIX
from mindflow.core.prompts import PR_TITLE_PREFIX


def run_pr(args: Tuple[str], title: Optional[str] = None, body: Optional[str] = None):
    if (base_branch_name := get_flag_values_from_args(args, ["--base", "-B"])) is None:
        base_branch_name = (
            subprocess.check_output(["git", "symbolic-ref", "refs/remotes/origin/HEAD"])
            .decode()
            .strip()
            .split("/")[-1]
        )

    if not title or not body:
        title, body = create_title_and_body(base_branch_name, title, body) or (
            None,
            None,
        )

    if not title or not body:
        return

    print(
        execute_command_and_print_without_trace(
            ["gh", "pr", "create"] + list(args) + ["--title", title, "--body", body]
        )
    )


def create_title_and_body(
    base_branch, title: Optional[str], body: Optional[str]
) -> Optional[Tuple[str, str]]:
    settings = Settings()
    completion_model = settings.mindflow_models.query.model

    diff_output = run_diff((base_branch,))
    if not diff_output:
        diff_output = ""

    title_response: Union[ModelError, str]
    body_response: Union[ModelError, str]
    if title is None and body is None:
        pr_title_prompt = build_prompt_from_conversation_messages(
            [
                create_conversation_message(Role.SYSTEM.value, PR_TITLE_PREFIX),
                create_conversation_message(Role.USER.value, diff_output),
            ],
            completion_model,
        )
        pr_body_prompt = build_prompt_from_conversation_messages(
            [
                create_conversation_message(Role.SYSTEM.value, PR_BODY_PREFIX),
                create_conversation_message(Role.USER.value, diff_output),
            ],
            completion_model,
        )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_title = executor.submit(
                settings.mindflow_models.query.model, pr_title_prompt
            )
            future_body = executor.submit(
                settings.mindflow_models.query.model, pr_body_prompt
            )

        title_response = future_title.result()
        body_response = future_body.result()
    else:
        if title is None:
            pr_title_prompt = build_prompt_from_conversation_messages(
                [
                    create_conversation_message(Role.SYSTEM.value, PR_TITLE_PREFIX),
                    create_conversation_message(Role.USER.value, diff_output),
                ],
                completion_model,
            )
            title_response = completion_model(pr_title_prompt)
        if body is None:
            pr_body_prompt = build_prompt_from_conversation_messages(
                [
                    create_conversation_message(Role.SYSTEM.value, PR_BODY_PREFIX),
                    create_conversation_message(Role.USER.value, diff_output),
                ],
                completion_model,
            )
            body_response = completion_model(pr_body_prompt)

    if isinstance(title_response, ModelError):
        print(title_response.pr_message)
        return None
    if isinstance(body_response, ModelError):
        print(body_response.pr_message)
        return None

    return (
        title if title is not None else title_response,
        body if body is not None else body_response,
    )
