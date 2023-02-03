"""
Command Line Client for Mindflow
"""

import argparse
import sys
from typing import Tuple

from mindflow.cli.parser import get_parsed_cli_args
from mindflow.db.static_definition import JSON_DB_PATH, ObjectStoreType
from mindflow.input import Arguments, Command, DBConfig
from mindflow.state import ConfiguredModel, ConfiguredService, STATE

from mindflow.commands.ask import ask
from mindflow.commands.config import config
from mindflow.commands.delete import delete
from mindflow.commands.diff import diff
from mindflow.commands.index import index
from mindflow.commands.inspect import inspect
from mindflow.commands.query import query

MF_DESCRIPTION = """

Welcome to Mindflow. A command line tool for intelligent development and collaboration.

"""

MF_USAGE = """

mf <command> [<args>]

ask        `mf ask <PROMPT>`                           Ask a question and get a prompt.
config     `mf config`                                 Configure Mindflow.
diff       `mf diff [<git diff args>]`                 Runs a `git diff` and summarizes the changes.
index      `mf index [<document paths>]`              Generate index of files/folders.
query      `mf query <YOUR QUERY> [<document paths>]`  Query your files/folders.
delete     `mf delete <document paths>`                   Delete a file/folder from Mindflow.
refresh    `mf refresh <document paths>`                  Refresh Mindflow index by regenerating already existing document indexes.
inspect    `mf inspect <document paths>`                  Inspect a file/folder in the Mindflow index.

"""


def cli() -> Tuple[str, dict, str, str]:
    # Parse Arguments
    parser = set_parser()
    args = parser.parse_args(arg.upper() for arg in sys.argv[1:2])
    command = Command[args.command].value
    args = get_parsed_cli_args(command)
    arguments = {
        "document_paths": args.document_paths
        if hasattr(args, "document_paths")
        else None,
        "force": args.force if hasattr(args, "force") else None,
        "index": args.index if hasattr(args, "index") else None,
        "git_diff_args": args.git_diff_args if hasattr(args, "git_diff_args") else None,
        "query": args.query if hasattr(args, "query") else None,
        "skip_clipboard": args.skip_clipboard
        if hasattr(args, "skip_clipboard")
        else None,
    }

    # Configure State
    STATE.db_config = DBConfig(ObjectStoreType.JSON.value, JSON_DB_PATH)
    STATE.configured_service = ConfiguredService(STATE.db_config)
    STATE.configured_model = ConfiguredModel(
        command, STATE.configured_service, STATE.db_config
    )
    STATE.arguments = Arguments(arguments)
    STATE.command = command

    # Execute Command
    match command:
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


def set_parser():
    parser = argparse.ArgumentParser(description=MF_DESCRIPTION, usage=MF_USAGE)
    parser.add_argument(
        "command",
        choices=Command.__members__,
        help="The command to execute",
    )
    return parser
