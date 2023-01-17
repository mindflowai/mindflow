"""
This module contains the main CLI for Mindflow.
"""
import argparse
import sys
from typing import List

from mindflow.utils.prompting.prompt_generator import generate_diff_prompt
from mindflow.utils.response import handle_response_text
from mindflow.requests.prompt import request_prompt
from mindflow.resolve_handling.resolve import resolve
from mindflow.resolve_handling.resolvers.base_resolver import Resolved
from mindflow.utils.token import set_token
from mindflow.resolve_handling.generate_index import generate_index
from mindflow.requests.query import request_query

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


"""


def _add_generate_args(parser):
    """
    Add arguments for the generate command.
    """
    parser.add_argument(
        "-i",
        "--index",
        action="store_true",
        help="Generate an index the references.",
    )


def _add_reference_args(parser):
    """
    Add arguments for commands that require references to text.
    """
    parser.add_argument(
        "references",
        nargs="+",
        help="A list of references to summarize (file path, API, web address).",
    )


def _add_query_args(parser):
    """
    Add arguments for commands that require references to text.
    """
    parser.add_argument(
        "query", type=str, help="The query you want to make on some data."
    )


def _add_diff_args(parser):
    """
    Add arguments for the diff command.
    """
    parser.add_argument(
        "diffargs",
        nargs="*",
        help="Contains all of the git diff args.",
    )


def _add_auth_args(parser):
    """
    Add arguments for the diff command.
    """
    # Argument for JWT token (optional)
    parser.add_argument(
        "token",
        type=str,
        nargs="?",
        help="JWT token used to authorize usage.",
    )


def _add_ask_args(parser):
    """
    Add arguments for commands that require references to text.
    """
    parser.add_argument("prompt", type=str, help="Prompt for GPT model.")


def _add_response_args(parser):
    parser.add_argument(
        "-p",
        "--return-prompt",
        action="store_true",
        help="Generate prompt only.",
    )
    parser.add_argument(
        "-s",
        "--skip-clipboard",
        action="store_true",
        help="Do not copy to clipboard (testing).",
    )


class MindFlow:
    """
    This class is the CLI for Mindflow.
    """

    def __init__(self):
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

    def auth(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        parser = argparse.ArgumentParser(
            description="Authorize User.",
        )
        _add_auth_args(parser)
        args = parser.parse_args(sys.argv[2:])
        set_token(args.token)

    def ask(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        parser = argparse.ArgumentParser(
            description="Prompt GPT model with basic request.",
        )
        _add_ask_args(parser)
        _add_response_args(parser)

        args = parser.parse_args(sys.argv[2:])
        response: str = request_prompt(args.prompt, True).text
        handle_response_text(response, args.skip_clipboard)

    def diff(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        parser = argparse.ArgumentParser(
            description="Summarize a git diff.",
        )
        _add_diff_args(parser)
        _add_response_args(parser)

        args = parser.parse_args(sys.argv[2:])
        prompt: str = generate_diff_prompt(args.diffargs)
        response: str = request_prompt(prompt, True).text
        handle_response_text(response, args.skip_clipboard)

    def generate(self):
        """
        This function is used to generate an index and/or embeddings for files
        """
        parser = argparse.ArgumentParser(
            description="Generate an index and/or embeddings for files.",
        )
        _add_reference_args(parser)
        _add_generate_args(parser)
        _add_response_args(parser)

        args = parser.parse_args(sys.argv[2:])
        resolved_references: List[Resolved] = []
        for reference in args.references:
            resolved_references.extend(resolve(reference))

        generate_index(resolved_references)

    def query(self):
        """
        This function is used to ask a custom question about files, folders, and websites.
        """
        parser = argparse.ArgumentParser(
            description="This command is use to query files, folders, and websites.",
        )
        _add_query_args(parser)
        _add_reference_args(parser)
        _add_generate_args(parser)
        _add_response_args(parser)

        args = parser.parse_args(sys.argv[2:])
        resolved_references: List[Resolved] = []
        for reference in args.references:
            resolved_references.extend(resolve(reference))

        if args.index:
            generate_index(resolved_references)

        reference_hashes: List[str] = [
            reference.text_hash for reference in resolved_references
        ]
        response: str = request_query(
            args.query, reference_hashes, True
        ).text
        handle_response_text(response, args.skip_clipboard)

    # Alias for query
    def q(self):
        """
        Query Alias
        """
        return self.query()


def main():
    """
    This is the main function.
    """
    MindFlow()
