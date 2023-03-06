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
    response: str = settings.mindflow_models.query.model([{"role": "system", "content": "You are a helpful virtual assistant responding to a users query using your general knowledge and the text provided below."}, {"role": "user", "content": prompt}])
    print(response)
