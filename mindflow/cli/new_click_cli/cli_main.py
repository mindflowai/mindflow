import click

from mindflow.cli.new_click_cli.config_cli import login

@click.group()
def mindflow_cli():
    pass

mindflow_cli.add_command(login)

if __name__ == '__main__':
    mindflow_cli()