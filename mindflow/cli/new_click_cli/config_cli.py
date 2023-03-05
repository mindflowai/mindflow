import click

from mindflow.utils.auth import write_openai_api_key_to_file

@click.command(help="Set your OpenAI API Key. You can get this from `https://platform.openai.com/account/api-keys`")
@click.argument("openai_api_key")
def login(openai_api_key):
    write_openai_api_key_to_file(openai_api_key)