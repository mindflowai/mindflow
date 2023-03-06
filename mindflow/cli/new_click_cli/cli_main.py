import click

from mindflow.cli.new_click_cli.commands.login import login
# from mindflow.cli.new_click_cli.commands.config import config
from mindflow.cli.new_click_cli.commands.ask import ask

@click.group()
def mindflow_cli():
    pass

mindflow_cli.add_command(login)
mindflow_cli.add_command(ask)
# mindflow_cli.add_command(config)

if __name__ == '__main__':
    mindflow_cli()