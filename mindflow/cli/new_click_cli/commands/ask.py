"""
`ask` command
"""

import click

from mindflow.core.ask import run_ask

@click.command(help="")
@click.argument("prompt", type=str)
def ask(prompt: str) -> str:
    """
    This function is used to generate a prompt and then use it as a prompt for GPT bot.
    """
    print(run_ask(prompt))
