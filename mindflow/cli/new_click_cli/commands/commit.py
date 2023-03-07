import click

from typing import Tuple
from mindflow.core.commit import run_commit
from mindflow.cli.new_click_cli.util import passthrough_command


@passthrough_command(help="Generate a git commit response by feeding git diff to gpt")
def commit(args: Tuple[str]):
    """
    Commit command.
    """
    print(run_commit(args))
