"""
This module contains the main CLI for Mindflow.
"""
import argparse
import sys

from mindflow.utils.login_credentials import get_login_credentials

try:
    from mindflow.models.chat_gpt import get_chat_gpt
except ImportError:
    pass
from mindflow.prompt_generator import generate_diff_prompt
from mindflow.prompt_generator import generate_prompt_from_files
from mindflow.utils.git import check_is_git_repo
from mindflow.utils.response import get_response


COPY_TO_CLIPBOARD = True

MF_DESCRIPTION = """

Welcome to Mindflow. A command line tool for intelligent development and collaboration.

"""

MF_USAGE = """

mf <command> [<args>]
The commands available in this CLI are:

diff       Runs a `git diff` and summarizes the changes.
query      Ask a query using all or a subset of your notes as a reference.

"""


def _add_reference_args(parser):
    """
    Add arguments for commands that require references to text.
    """
    parser.add_argument(
        "references",
        nargs="+",
        help="A list of references to summarize (file path, API, web address).",
    )
    parser.add_argument(
        "-s",
        "--skip-response",
        action="store_true",
        help="Generate prompt only.",
    )
    parser.add_argument(
        "-t",
        "--skip-clipboard",
        action="store_true",
        help="Do not copy to clipboard (testing).",
    )


def _add_diff_args(parser):
    """
    Add arguments for the diff command.
    """
    parser.add_argument(
        "diffargs",
        nargs="*",
        help="This argument is used to pass to git diff.",
    )
    parser.add_argument(
        "-s",
        "--skip-response",
        action="store_true",
        help="Generate prompt only.",
    )
    parser.add_argument(
        "-t",
        "--skip-clipboard",
        action="store_true",
        help="Do not copy to clipboard (testing).",
    )


class MindFlow:
    """
    This class is the CLI for Mindflow.
    """

    def __init__(self):
        self.login_credentials = get_login_credentials()
        check_is_git_repo()

        parser = argparse.ArgumentParser(
            description=MF_DESCRIPTION,
            usage=MF_USAGE,
        )
        parser.add_argument("command", help="Subcommand to run")
        args = parser.parse_args(sys.argv[1:2])

        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            sys.exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def _handle_prompt(self, args, prompt: str):
        if args.skip_response:
            print(prompt)
        else:
            response = get_response(self.model, prompt)
            print("\n\n\n\n")
            print("----------------RESPONSE FROM MODEL----------------")
            print(response)
            print("---------------------------------------------------")
            print("\n")

    def diff(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        self.model = get_chat_gpt(self.login_credentials)
        parser = argparse.ArgumentParser(
            description="Summarize a git diff.",
        )

        _add_diff_args(parser)

        args = parser.parse_args(sys.argv[2:])
        prompt = generate_diff_prompt(args)
        self._handle_prompt(args, prompt)

    def query(self):
        """
        This function is used to ask a custom question about any number of files, folders, and websites.
        """
        self.model = get_chat_gpt(self.login_credentials)
        parser = argparse.ArgumentParser(
            description="This command is use to query files, folders, and websites.",
        )

        parser.add_argument(
            "query", type=str, help="The query you want to make on some data."
        )

        _add_reference_args(parser)

        args = parser.parse_args(sys.argv[2:])
        prompt = generate_prompt_from_files(args, self.model, args.query)
        self._handle_prompt(args, prompt)
    
    def config(self):
        """
        This function is used to ask a custom question about any number of files, folders, and websites.
        """
        get_login_credentials(create_new=True)

    # Alias for query
    def q(self):
        return self.query()


def main():
    """
    This is the main function.
    """
    MindFlow()
