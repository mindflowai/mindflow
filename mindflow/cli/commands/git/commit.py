import asyncio
from typing import Tuple, Optional

import click
from result import Err, Result

from mindflow.cli.util import passthrough_command
from mindflow.core.commands.git.commit import create_gpt_commit_message
from mindflow.core.execute import execute_command_without_trace
from mindflow.core.settings import Settings
from mindflow.core.types.model import ModelApiCallError


@passthrough_command(help="Generate a git commit response by feeding git diff to gpt")
# @overloaded_option(
#     "-m",
#     "--message",
#     help="Don't use mindflow to generate a commit message, use this one instead.",
#     default=None,
# )
@click.option(
    "-m",
    "--message",
    help="Don't use mindflow to generate a commit message, use this one instead.",
    default=None,
)
def commit(args: Tuple[str], message: Optional[str] = None):
    if message is not None:
        click.echo(
            f"Warning: Using message '{message}' instead of mindflow generated message."
        )
        click.echo("It's recommended that you don't use the -m/--message flag.")

    if not message:
        diff_output = execute_command_without_trace(["git", "diff", "--cached"])
        run_commit_result: Result[str, ModelApiCallError] = asyncio.run(
            create_gpt_commit_message(Settings(), diff_output)
        )
        if isinstance(run_commit_result, Err):
            print(run_commit_result.value)
            return
        message = run_commit_result.value

    click.echo(
        execute_command_without_trace(["git", "commit", "-m", message] + list(args))
    )
