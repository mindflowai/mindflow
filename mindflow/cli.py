"""
Command Line Client for Mindflow
"""

import argparse
from enum import Enum
import sys

from mindflow.commands.diff import Diff
from mindflow.commands.ask import Ask
from mindflow.commands.auth import Auth
from mindflow.commands.generate import Generate
from mindflow.commands.query import Query
from mindflow.commands.refresh import Refresh
from mindflow.commands.delete import Delete


MF_DESCRIPTION = """

Welcome to Mindflow. A command line tool for intelligent development and collaboration.

"""

MF_USAGE = """

mf <command> [<args>]

ask        `mf ask <PROMPT>`                           Ask a question and get a prompt.
diff       `mf diff [<git diff args>]`                 Runs a `git diff` and summarizes the changes.
generate   `mf generate [<Files + Folders>]`           Generate index of files/folders in Mindflow Server.
query      `mf query <YOUR QUERY> [<Files + Folders>]` Query your files/folders.
auth       `mf auth <AUTH TOKEN>`                      Authorize Mindflow with JWT.
refresh    `mf refresh`                                Deletes Mindflow Index and optionally regenerates it.

"""


class CommandLineInterface:
    """
    Command Line Client for Mindflow
    """

    class Commands(Enum):
        """
        Arguments for the command line client
        """

        GENERATE = Generate
        QUERY = Query
        AUTH = Auth
        DIFF = Diff
        ASK = Ask
        REFRESH = Refresh
        DELETE = Delete

    def __init__(self):
        parser = argparse.ArgumentParser(description=MF_DESCRIPTION, usage=MF_USAGE)

        parser.add_argument(
            "command",
            choices=[c.name for c in CommandLineInterface.Commands],
            help="The command to execute",
        )

        args = parser.parse_args(arg.upper() for arg in sys.argv[1:2])
        self.cmd = CommandLineInterface.Commands[args.command].value()

    def execute(self):
        """
        Execute command (Polymorphic)
        """
        self.cmd.execute()
