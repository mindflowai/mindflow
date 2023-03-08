from typing import Optional, Tuple

import click
from mindflow.cli.new_click_cli.util import passthrough_command
from mindflow.core.git.mr import run_mr


@click.group()
def mr():
    """
    MR command.
    """
    pass


@passthrough_command(
    help="Generate a git pr response by feeding git diff to gpt"
)
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
def create(args: Tuple[str], title: Optional[str] = None, body: Optional[str] = None):
    """
    PR command.
    """
    if title is not None:
        click.echo(
            f"Warning: Using message '{title}' instead of mindflow generated message."
        )
        click.echo("It's recommended that you don't use the -m/--message flag.")
    
    if body is not None:
        click.echo(
            f"Warning: Using message '{body}' instead of mindflow generated message."
        )
        click.echo("It's recommended that you don't use the -m/--message flag.")

    run_mr(args, title_overwrite=title, body_overwrite=body)


mr.add_command(create)
