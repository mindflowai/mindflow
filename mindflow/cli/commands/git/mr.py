import click
from typing import Optional, Tuple
from mindflow.cli.util import passthrough_command


@click.group()
def mr():
    """
    MR command.
    """
    pass


@passthrough_command(help="Generate a git pr response by feeding git diff to gpt")
@click.option(
    "-t",
    "--title",
    help="Don't use mindflow to generate a pr title, use this one instead.",
    default=None,
)
@click.option(
    "-d",
    "--description",
    help="Don't use mindflow to generate a pr body, use this one instead.",
    default=None,
)
def create(
    args: Tuple[str], title: Optional[str] = None, description: Optional[str] = None
):
    import asyncio
    import subprocess

    from result import Err

    from mindflow.cli.util import (
        execute_command_without_trace,
        get_flag_values_from_args,
    )
    from mindflow.core.commands.git.pr import create_gpt_title_and_body
    from mindflow.core.settings import Settings
    from termcolor import colored

    if title is not None:
        click.echo(
            colored(
                f"Warning: Using message '{title}' instead of mindflow generated message. It's recommended that you don't use the -t/--title flag.",
                "yellow",
            )
        )

    if description is not None:
        click.echo(
            colored(
                f"Warning: Using message '{description}' instead of mindflow generated message. It's recommended that you don't use the -d/--description flag.",
                "yellow",
            )
        )
    if (
        base_branch_name := get_flag_values_from_args(args, ["--target-branch", "-b"])
    ) is None:
        base_branch_name = (
            subprocess.check_output(["git", "symbolic-ref", "refs/remotes/origin/HEAD"])
            .decode()
            .strip()
            .split("/")[-1]
        )

    diff_result = execute_command_without_trace(
        ["git", "diff", base_branch_name]
    ).strip()

    if not title or not description:
        title_and_body_result = asyncio.run(
            create_gpt_title_and_body(Settings(), diff_result, title, description)
        )
        if isinstance(title_and_body_result, Err):
            click.echo(title_and_body_result.value)
            return
        title, description = title_and_body_result.value

    click.echo(
        execute_command_without_trace(
            ["glab", "mr", "create"]
            + list(args)
            + ["--title", title, "--description", description]
        )
    )


mr.add_command(create)
