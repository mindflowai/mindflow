import click

from mindflow.core.git.pr import run_pr


@click.command(help="Generate a git pr response by feeding git diff to gpt")
def pr():
    """
    PR command.
    """
    run_pr()
