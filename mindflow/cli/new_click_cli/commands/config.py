"""
`auth` command
"""
from mindflow.cli.config.main import set_configuration

import click


@click.command
def config():
    set_configuration()
