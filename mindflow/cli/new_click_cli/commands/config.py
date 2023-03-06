"""
`auth` command
"""
from mindflow.cli.config.main import set_configuration

import click


@click.command(help="Advanced setup custom mindflow configurations.")
def config():
    set_configuration()
