"""
Command Line Client for Mindflow
"""

import argparse
import sys

from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.state import STATE
from mindflow.input import Arguments, Command

from mindflow.cli.parser import get_parsed_cli_args
from mindflow.settings import Settings

from mindflow.core.ask import AskArgs, ask
from mindflow.cli.new_click_cli.commands.commit import commit
from mindflow.cli.new_click_cli.commands.config import config
from mindflow.cli.new_click_cli.commands.delete import DeleteArgs, delete
from mindflow.cli.new_click_cli.commands.diff import DiffArgs, diff
from mindflow.cli.new_click_cli.commands.index import IndexArgs, index
from mindflow.cli.new_click_cli.commands.inspect import InspectArgs, inspect
from mindflow.core.query import QueryArgs, query
from mindflow.utils.response import handle_response_text

MF_DESCRIPTION = """

Welcome to Mindflow. A command line tool for intelligent development and collaboration.

"""

MF_USAGE = """

mf <command> [<args>]

ask        `mf ask <PROMPT>`                              Ask a question and get a prompt.
commit     `mf commit [<git commit args>]`                Generate commit message and commit.
config     `mf config`                                    Configure Mindflow.
diff       `mf diff [<git diff args>]`                    Runs a `git diff` and summarizes the changes.
index      `mf index [<document paths>]`                  Generate index of files/folders.
query      `mf query <YOUR QUERY> [<document paths>]`     Query your files/folders.
delete     `mf delete <document paths>`                   Delete a file/folder from Mindflow.
refresh    `mf refresh <document paths>`                  Refresh Mindflow index by regenerating already existing document indexes.
inspect    `mf inspect <document paths>`                  Inspect a file/folder in the Mindflow index.

"""


def cli():
    # Parse Arguments
    parser = set_parser()
    args = parser.parse_args(arg.upper() for arg in sys.argv[1:2])
    command = Command[args.command].value
    args = get_parsed_cli_args(command)

    # Configure State
    settings = Settings()

    # Execute Command
    match command:
        case Command.ASK.value:
            response: str = ask(args.prompt, settings.mindflow_models.query)
            handle_response_text(response, )
        case Command.COMMIT.value:
            commit()
        case Command.CONFIG.value:
            config()
        case Command.DELETE.value:
            delete(args.document_paths)
        case Command.DIFF.value:
            diff(settings.mindflow_models.index)
        case Command.INSPECT.value:
            inspect(args.document_paths)
        case Command.QUERY.value:
            if hasattr(args, "index") and args.index:
                index(args.document_paths, Command.INDEX, args.force, settings.mindflow_models.index)
            query(args.document_paths, args.query, settings.mindflow_models.query, settings.mindflow_models.embedding)
        case Command.REFRESH.value:
            index(args.document_paths, Command.INDEX, args.force, settings.mindflow_models.index)
        case Command.INDEX.value:
            index(args.document_paths, Command.REFRESH, args.force, settings.mindflow_models.index)

    print("Saving database...")
    DATABASE_CONTROLLER.databases.json.save_file()


def set_parser():
    parser = argparse.ArgumentParser(description=MF_DESCRIPTION, usage=MF_USAGE)
    parser.add_argument(
        "command",
        choices=Command.__members__,
        help="The command to execute",
    )
    return parser
