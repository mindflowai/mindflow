"""
Arguments setters for CLI parser.
"""

import argparse
import sys

from mindflow.input import Command


# Command Parsers
def ask_args() -> argparse.Namespace:
    """
    Ask command parser.
    """
    parser = argparse.ArgumentParser(
        description="Ask a question.",
    )
    add_query_arg(parser)
    add_remote_arg(parser)
    add_return_prompt_arg(parser)
    add_skip_clipboard_arg(parser)
    return parser.parse_args(sys.argv[2:])


def config_args() -> argparse.Namespace:
    """
    Config command parser.
    """
    parser = argparse.ArgumentParser(
        description="Configure Mindflow.",
    )
    return parser.parse_args(sys.argv[2:])


def delete_args() -> argparse.Namespace:
    """
    Delete command parser.
    """
    parser = argparse.ArgumentParser(
        description="Delete a document.",
    )
    add_document_paths_arg(parser)
    add_remote_arg(parser)
    return parser.parse_args(sys.argv[2:])


def diff_args() -> argparse.Namespace:
    """
    Diff command parser.
    """
    parser = argparse.ArgumentParser(
        description="Summarize your git diff.",
    )
    add_diffargs_arg(parser)
    add_remote_arg(parser)
    add_return_prompt_arg(parser)
    add_skip_clipboard_arg(parser)
    return parser.parse_args(sys.argv[2:])


def index_args() -> argparse.Namespace:
    """
    Generate command parser.
    """
    parser = argparse.ArgumentParser(
        description="Generate an index.",
    )
    add_document_paths_arg(parser)
    return parser.parse_args(sys.argv[2:])


def inspect_args() -> argparse.Namespace:
    """
    Inspect command parser.
    """
    parser = argparse.ArgumentParser(
        description="Inspect your index.",
    )
    add_document_paths_arg(parser)
    add_remote_arg(parser)
    return parser.parse_args(sys.argv[2:])


def query_args() -> argparse.Namespace:
    """
    Query command parser.
    """
    parser = argparse.ArgumentParser(
        description="Query your index.",
    )
    add_document_paths_arg(parser)
    add_index_arg(parser)
    add_query_arg(parser)
    add_remote_arg(parser)
    add_return_prompt_arg(parser)
    add_skip_clipboard_arg(parser)
    return parser.parse_args(sys.argv[2:])


def refresh_args() -> argparse.Namespace:
    """
    Refresh command parser.
    """
    parser = argparse.ArgumentParser(
        description="Refresh your index.",
    )
    add_document_paths_arg(parser)
    add_remote_arg(parser)
    add_force_arg(parser)
    return parser.parse_args(sys.argv[2:])


# Argument setters
def add_remote_arg(parser: argparse.ArgumentParser):
    """
    Add arguments for commands that require a remote Mindflow server.
    """
    parser.add_argument(
        "-r",
        "--remote",
        action="store_true",
        help="Use the remote Mindflow server.",
    )


def add_index_arg(parser: argparse.ArgumentParser):
    """
    Add arguments for the generate command.
    """
    parser.add_argument(
        "-i",
        "--index",
        action="store_true",
        help="Generate an index for documents.",
    )


def add_document_paths_arg(parser: argparse.ArgumentParser):
    """
    Add arguments for handling document paths.
    """
    parser.add_argument(
        "document_paths",
        nargs="+",
        help="A list of document paths to summarize (file path, API, web address).",
    )


def add_query_arg(parser: argparse.ArgumentParser):
    """
    Add arguments for querying documents.
    """
    parser.add_argument(
        "query", type=str, help="The query you want to make on some data."
    )


def add_diffargs_arg(parser: argparse.ArgumentParser):
    """
    Add arguments for the diff command.
    """
    parser.add_argument(
        "diffargs",
        nargs="*",
        help="Contains all of the git diff args.",
    )


def add_return_prompt_arg(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-p",
        "--return-prompt",
        action="store_true",
        help="Generate prompt only.",
    )


def add_skip_clipboard_arg(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-s",
        "--skip-clipboard",
        action="store_true",
        help="Do not copy to clipboard (testing).",
    )


def add_force_arg(parser: argparse.ArgumentParser):
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Apply THE FORCE to your command.",
    )


def get_parsed_cli_args(command: str) -> argparse.Namespace:
    match command:
        case Command.ASK.value:
            return ask_args()
        case Command.CONFIG.value:
            return config_args()
        case Command.DELETE.value:
            return delete_args()
        case Command.DIFF.value:
            return diff_args()
        case Command.INDEX.value:
            return index_args()
        case Command.INSPECT.value:
            return inspect_args()
        case Command.QUERY.value:
            return query_args()
        case Command.REFRESH.value:
            return refresh_args()
        case _:
            raise ValueError(f"Invalid command: {command}")
