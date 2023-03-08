from typing import Optional, Tuple

import click
from mindflow.cli.new_click_cli.util import passthrough_command
from mindflow.core.git.mr import run_mr


@click.group()
def mr():
    """
    MindFlow powered GitLab Merge Request manager.
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
    """
    PR command.
    """
    if title is not None:
        click.echo(
            f"Warning: Using message '{title}' instead of mindflow generated message."
        )
        click.echo("It's recommended that you don't use the -t/--title flag.")

    if description is not None:
        click.echo(
            f"Warning: Using message '{description}' instead of mindflow generated message."
        )
        click.echo("It's recommended that you don't use the -d/--description flag.")

    # check if the `glab` command is available
    # try:
    #     # try running the glab command in the shell, if it fails, an exception will be raised
    #     click.echo("Checking if `glab` is installed...")
    #     subprocess.check_output(["glab", "--version"])

    # except click.exceptions.MissingParameter:
    #     
    #     exit()

    import subprocess

    try:
        subprocess.check_output(['glab', '--version'])
    except Exception:
        click.echo("The `glab` command is not available. Please install it here: https://docs.gitlab.com/ee/integration/glab/")
        exit()

    run_mr(args, title=title, description=description)


mr.add_command(create)
