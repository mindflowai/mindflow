import subprocess
from typing import Optional, Tuple

from mindflow.core.commands.git.pr import create_title_and_body
from mindflow.core.command_parse import get_flag_values_from_args
from mindflow.core.execute import execute_command_and_print_without_trace


def run_mr(
    args: Tuple[str], title: Optional[str] = None, description: Optional[str] = None
):
    if (
        base_branch_name := get_flag_values_from_args(args, ["--target-branch", "-b"])
    ) is None:
        base_branch_name = (
            subprocess.check_output(["git", "symbolic-ref", "refs/remotes/origin/HEAD"])
            .decode()
            .strip()
            .split("/")[-1]
        )

    if not title or not description:
        title, description = create_title_and_body(
            base_branch_name, title, description
        ) or (
            None,
            None,
        )

    if not title or not description:
        return

    print(
        execute_command_and_print_without_trace(
            ["glab", "mr", "create"]
            + list(args)
            + ["--title", title, "--description", description]
        )
    )
