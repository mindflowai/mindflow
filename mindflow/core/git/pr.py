import concurrent.futures
import subprocess
from typing import List, Optional, Tuple, Union

from mindflow.core.git.diff import run_diff
from mindflow.settings import Settings
from mindflow.utils.command_parse import get_flag_value
from mindflow.utils.errors import ModelError
from mindflow.utils.execute import execute_no_trace
from mindflow.utils.prompt_builders import build_context_prompt
from mindflow.utils.prompts import PR_BODY_PREFIX
from mindflow.utils.prompts import PR_TITLE_PREFIX


def run_pr(args: Tuple[str], title: Optional[str] = None, body: Optional[str] = None):
    base_branch = get_flag_value(args, ["--base", "-B"])

    if base_branch is None:
        # Determine the name of the default branch
        base_branch = (
            subprocess.check_output(["git", "symbolic-ref", "refs/remotes/origin/HEAD"])
            .decode()
            .strip()
            .split("/")[-1]
        )

    if not title or not body:
        title_body_tuple = create_title_and_body(base_branch, title, body)

    if not title_body_tuple:
        return

    title, body = title_body_tuple

    command: List[str] = ["gh", "pr", "create"] + list(args) + ["--title", title, "--body", body]  # type: ignore
    print(execute_no_trace(command))


def create_title_and_body(
    base_branch, title: Optional[str], body: Optional[str]
) -> Optional[Tuple[str, str]]:
    settings = Settings()

    diff_output = run_diff((base_branch,))
    if not diff_output:
        diff_output = ""

    title_response: Union[ModelError, str]
    body_response: Union[ModelError, str]
    if title is None and body is None:
        pr_title_prompt = build_context_prompt(PR_TITLE_PREFIX, diff_output)
        pr_body_prompt = build_context_prompt(PR_BODY_PREFIX, diff_output)

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
            pr_title_prompt = build_context_prompt(PR_TITLE_PREFIX, diff_output)
            title_response = settings.mindflow_models.query.model(pr_title_prompt)
        if body is None:
            pr_body_prompt = build_context_prompt(PR_BODY_PREFIX, diff_output)
            body_response = settings.mindflow_models.query.model(pr_body_prompt)

    if isinstance(title_response, ModelError):
        print(title_response.pr_message)
        return None
    if isinstance(body_response, ModelError):
        print(body_response.pr_message)
        return None

    title = title if title is not None else title_response
    body = body if body is not None else body_response
    return title, body
