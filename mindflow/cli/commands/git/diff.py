import asyncio
from typing import Tuple
import click
from result import Err

from mindflow.cli.util import passthrough_command
from mindflow.core.commands.git.diff import create_gpt_summarized_diff
from mindflow.core.execute import execute_command_without_trace
from mindflow.core.settings import Settings


@passthrough_command(
    help="Wrapper around git diff that summarizes the output. Treat this command exactly like git diff, it supports all arguments that git diff provides."
)
@click.option("--detailed", type=bool, default=False, is_flag=True)
def diff(args: Tuple[str], detailed: bool):
    diff_output = execute_command_without_trace(["git", "diff"] + list(args)).strip()
    if not diff_output:
        click.echo("No diff output to summarize.")
        return

    if not detailed:
        click.echo(
            "Working on a summary of the diff, use the `--detailed` flag to show a much more thorough breakdown of the diff...\n"
        )

    summarize_diff_result = asyncio.run(
        create_gpt_summarized_diff(Settings(), diff_output, detailed=detailed)
    )
    if isinstance(summarize_diff_result, Err):
        click.echo(summarize_diff_result.value)
        return

    click.echo(summarize_diff_result.value)
