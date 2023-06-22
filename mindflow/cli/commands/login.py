import click

from mindflow.core.commands.login import run_login


@click.command(help="Set your API Key")
def login():
    run_login()
