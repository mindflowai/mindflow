import concurrent.futures
import subprocess
from typing import List, Optional, Tuple, Union

from mindflow.core.git.diff import run_diff
from mindflow.settings import Settings
from mindflow.utils.command_parse import get_flag_value
from mindflow.utils.errors import ModelError
from mindflow.utils.prompt_builders import build_context_prompt
from mindflow.utils.prompts import PR_BODY_PREFIX
from mindflow.utils.prompts import PR_TITLE_PREFIX


def run_pr(args: Tuple[str], title: Optional[str] = None, body: Optional[str] = None):
    base_branch = get_flag_value(args, ["--base", "-B"])
    head_branch = get_flag_value(args, ["--head", "-H"])

    if base_branch is None:
        # Determine the name of the default branch
        base_branch = (
            subprocess.check_output(["git", "symbolic-ref", "refs/remotes/origin/HEAD"])
            .decode()
            .strip()
            .split("/")[-1]
        )

    if head_branch is None:
        # Get the name of the current branch
        head_branch = (
            subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"])
            .decode("utf-8")
            .strip()
        )

    if not is_valid_pr(base_branch, head_branch):
        return

    if not title or not body:
        tital_body_tuple = create_title_and_body(base_branch, title, body)

    if not tital_body_tuple:
        return

    title, body = tital_body_tuple
    create_pull_request(args, title, body)


def is_valid_pr(head_branch: str, base_branch: str) -> bool:
    if head_branch == base_branch:
        print("Cannot create pull request from default branch")
        return False

    if not has_remote_branch(head_branch):
        print("No remote branch for current branch")
        return False

    if needs_push():
        print("Current branch needs to be pushed to remote repository")
        return False

    return True


def create_title_and_body(
    base_branch, title: Optional[str], body: Optional[str]
) -> Optional[Tuple[str, str]]:
    settings = Settings()

    diff_output = run_diff((base_branch,))

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


def needs_push() -> bool:
    """
    Returns True if the current branch needs to be pushed to a remote repository, False otherwise.
    """
    # Get the output of `git status`
    git_status = subprocess.check_output(["git", "status"]).decode("utf-8")

    # Check if the output contains the message "Your branch is ahead of 'origin/<branch>' by <num> commit(s), and can be fast-forwarded."
    return "Your branch is ahead of" in git_status


def has_remote_branch(head_branch: str) -> bool:
    """
    Returns True if there is a remote branch for the current branch, False otherwise.
    """
    # Check if there is a remote branch for the current branch
    try:
        subprocess.check_output(
            ["git", "ls-remote", "--exit-code", "--heads", "origin", head_branch]
        )
        return True
    except subprocess.CalledProcessError:
        return False


def create_pull_request(args: Tuple[str], title: str, body: str):
    command: List[str] = ["gh", "pr", "create"] + list(args) + ["--title", title, "--body", body]  # type: ignore
    pr_result = subprocess.check_output(command).decode("utf-8")
    if "https://" in pr_result:
        print("Pull request created successfully")
        print(pr_result)
    else:
        print(
            "Failed to create pull request. Please raise an issue at: https://github.com/nollied/mindflow-cli/issues"
        )
        exit()
