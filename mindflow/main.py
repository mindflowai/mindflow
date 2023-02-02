"""
Main
"""


from mindflow.input import Command
from mindflow.state import STATE

from mindflow.commands.ask import ask
from mindflow.commands.config import config
from mindflow.commands.delete import delete
from mindflow.commands.diff import diff
from mindflow.commands.index import index
from mindflow.commands.inspect import inspect
from mindflow.commands.query import query


def main():
    """
    This is the main function.
    """
    match STATE.command:
        case Command.ASK.value:
            ask()
        case Command.CONFIG.value:
            config()
        case Command.DELETE.value:
            delete()
        case Command.DIFF.value:
            diff()
        case Command.INSPECT.value:
            inspect()
        case Command.QUERY.value:
            query()
        case Command.REFRESH.value:
            index()
        case Command.INDEX.value:
            index()
