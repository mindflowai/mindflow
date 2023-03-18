import click

from mindflow.cli.new_click_cli.commands.git.add import add
from mindflow.cli.new_click_cli.commands.git.push import push
from mindflow.cli.new_click_cli.commands.git.commit import commit
from mindflow.cli.new_click_cli.commands.git.diff import diff
from mindflow.cli.new_click_cli.commands.git.mr import mr
from mindflow.cli.new_click_cli.commands.git.pr import pr

from mindflow.cli.new_click_cli.commands.chat import chat, history
from mindflow.cli.new_click_cli.commands.delete import delete
from mindflow.cli.new_click_cli.commands.index import index
from mindflow.cli.new_click_cli.commands.inspect import inspect
from mindflow.cli.new_click_cli.commands.login import login
from mindflow.cli.new_click_cli.commands.gen import gen
from mindflow.cli.new_click_cli.commands.config import config

# from mindflow.cli.new_click_cli.commands.config import config


@click.group()
def mindflow_cli():
    pass


@mindflow_cli.command()
def version():
    """Get the currently installed version of mindflow."""
    from mindflow import __version__

    click.echo(__version__)


mindflow_cli.add_command(login)
mindflow_cli.add_command(chat)
mindflow_cli.add_command(commit)
mindflow_cli.add_command(history)
mindflow_cli.add_command(gen)
mindflow_cli.add_command(index)
mindflow_cli.add_command(inspect)
mindflow_cli.add_command(add)
mindflow_cli.add_command(push)
mindflow_cli.add_command(delete)
mindflow_cli.add_command(diff)
mindflow_cli.add_command(mr)
mindflow_cli.add_command(pr)
mindflow_cli.add_command(config)

if __name__ == "__main__":
    mindflow_cli()
