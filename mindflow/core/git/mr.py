import subprocess
from typing import Optional, Tuple, List

from mindflow.core.git.pr import create_title_and_body
from mindflow.utils.command_parse import get_flag_value
from mindflow.utils.execute import execute_no_trace


def run_mr(
    args: Tuple[str], title: Optional[str] = None, description: Optional[str] = None
):
    base_branch = get_flag_value(args, ["--target-branch", "-b"])

    if base_branch is None:
        # Determine the name of the default branch
        base_branch = (
            subprocess.check_output(["git", "symbolic-ref", "refs/remotes/origin/HEAD"])
            .decode()
            .strip()
            .split("/")[-1]
        )

    if not title or not description:
        tital_description_tuple = create_title_and_body(base_branch, title, description)

    if not tital_description_tuple:
        return

    title, description = tital_description_tuple

    command: List[str] = ["glab", "mr", "create"] + list(args) + ["--title", title, "--description", description]  # type: ignore
    print(execute_no_trace(command))
