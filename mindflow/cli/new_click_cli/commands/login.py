import click

from mindflow.core.login import run_login


@click.command(
    help="Set your OpenAI API Key. You can get this from `https://platform.openai.com/account/api-keys`"
)
@click.argument("openai_api_key")
def login(openai_api_key):
    run_login(openai_api_key)
