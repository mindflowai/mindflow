import click

from mindflow.core.commit import run_commit

@click.command(help="Generate a git commit response by feeding git diff to gpt")
def commit():
    """
    Commit command.
    """
    print(run_commit())
