import subprocess
from typing import Optional, Tuple, List

from mindflow.core.git.pr import create_title_and_body, is_valid_pr
from mindflow.utils.command_parse import get_flag_value

def run_mr(args: Tuple[str], title: Optional[str] = None, body: Optional[str] = None) -> str:
    base_branch = get_flag_value(args, ['--target-branch', '-b'])
    head_branch = get_flag_value(args, ['--source-branch', '-s'])

    if not is_valid_pr(get_flag_value(args, base_branch, head_branch)):
        return

    if not title or not body:
        title, body = create_title_and_body(base_branch, title, body)

    create_merge_request(args, title, body)

def create_merge_request(args: Tuple[str], title: str, body: str):
    command: List[str] = ["glab", "pr", "create"] + + list(args) + ["--title", title, "--description", body] # type: ignore
    pr_result = subprocess.check_output(command).decode("utf-8")
    if "https://" in pr_result:
        print("Merge request created successfully")
        print(pr_result)
    else:
        print(
            "Failed to create pull request. Please raise an issue at: https://github.com/nollied/mindflow-cli/issues"
        )
        exit()
