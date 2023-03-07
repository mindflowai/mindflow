"""
`ask` command
"""
import click

from mindflow.core.chat import run_chat


@click.command(help="")
@click.argument("prompt", type=str)
def chat(prompt: str):
    """
    This function is used to generate a prompt and then use it as a prompt for GPT bot.
    """
    print(run_chat(prompt))
