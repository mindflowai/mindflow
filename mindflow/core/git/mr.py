import subprocess
from typing import Optional, Tuple, List

from mindflow.core.git.pr import create_title_and_body, is_valid_pr
from mindflow.utils.command_parse import get_flag_value


def run_mr(
    args: Tuple[str], title: Optional[str] = None, description: Optional[str] = None
):
    base_branch = get_flag_value(args, ["--target-branch", "-b"])
    head_branch = get_flag_value(args, ["--source-branch", "-s"])

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

    if not title or not description:
        tital_description_tuple = create_title_and_body(base_branch, title, description)

    if not tital_description_tuple:
        return

    title, description = tital_description_tuple

    create_merge_request(args, title, description)


def create_merge_request(args: Tuple[str], title: str, description: str):
    command: List[str] = ["glab", "mr", "create"] + list(args) + ["--title", title, "--description", description]  # type: ignore
    pr_result = subprocess.check_output(command).decode("utf-8")
    if "https://" in pr_result:
        print("Merge request created successfully")
        print(pr_result)
    else:
        print(
            "Failed to create pull request. Please raise an issue at: https://github.com/nollied/mindflow-cli/issues"
        )
        exit()
