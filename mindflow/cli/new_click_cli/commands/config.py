"""
`auth` command
"""
import click

from mindflow.cli.config.main import set_configuration


@click.command(help="Advanced setup custom mindflow configurations.")
def config():
    set_configuration()
