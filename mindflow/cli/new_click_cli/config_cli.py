import click

from mindflow.utils.auth import write_key_to_file, OPENAI_API_KEY_LINK

@click.command(help=f"Set your OpenAI API Key. You can get this from `{OPENAI_API_KEY_LINK}`")
@click.argument("openai_api_key")
def login(openai_api_key):
    write_key_to_file(openai_api_key)