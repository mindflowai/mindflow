import click
from typing import Tuple

from mindflow.cli.util import passthrough_command


@passthrough_command(
    help="Wrapper around git diff that summarizes the output. Treat this command exactly like git diff, it supports all arguments that git diff provides."
)
@click.option("--detailed", type=bool, default=False, is_flag=True)
def diff(args: Tuple[str], detailed: bool):
    import asyncio

    from mindflow.core.commands.git.diff import create_gpt_summarized_diff
    from mindflow.cli.util import execute_command_without_trace
    from mindflow.core.settings import Settings
    from termcolor import colored
    from result import Ok

    diff_output = execute_command_without_trace(["git", "diff"] + list(args)).strip()
    if not diff_output:
        click.echo("No diff output to summarize.")
        return

    if not detailed:
        click.echo(
            colored(
                "Working on a summary of the diff, use the `--detailed` flag to show a much more thorough breakdown of the diff...\n",
                "yellow",
            )
        )

    async def stream_diff(settings: Settings, diff_output: str, detailed: bool):
        click.echo(colored("GPT:", attrs=["bold"]))
        async for char_stream_chunk in create_gpt_summarized_diff(
            settings, diff_output, detailed=detailed
        ):
            if isinstance(char_stream_chunk, Ok):
                click.echo(char_stream_chunk.value, nl=False)
            else:
                click.echo(char_stream_chunk.value)

    asyncio.run(stream_diff(Settings(), diff_output, detailed=detailed))
