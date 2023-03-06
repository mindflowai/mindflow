"""
`ask` command
"""

from mindflow.db.objects.model import Model
import click

@click.command()
@click.argument("prompt", type=str)
def ask(prompt: str, completion_model: Model) -> str:
    """
    This function is used to generate a prompt and then use it as a prompt for GPT bot.
    """
    # Prompt GPT through Mindflow API or locally
    return completion_model(prompt)
