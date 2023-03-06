"""
`ask` command
"""

from mindflow.db.objects.model import Model
import click

from mindflow.settings import Settings

@click.command(help="")
@click.argument("prompt", type=str)
def ask(prompt: str) -> str:
    """
    This function is used to generate a prompt and then use it as a prompt for GPT bot.
    """
    settings = Settings()
    # Prompt GPT through Mindflow API or locally
    return settings.mindflow_models.query(prompt)
