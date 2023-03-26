import click

from mindflow.core.login import run_login


@click.command(help="Set your API Key")
def login():
    run_login()
