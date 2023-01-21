import argparse


def _add_remote_args(parser: argparse.ArgumentParser):
    """
    Add arguments for commands that require a remote Mindflow server.
    """
    parser.add_argument(
        "-r",
        "--remote",
        action="store_true",
        help="Use the remote Mindflow server.",
    )


def _add_generate_args(parser: argparse.ArgumentParser):
    """
    Add arguments for the generate command.
    """
    parser.add_argument(
        "-i",
        "--index",
        action="store_true",
        help="Generate an index the references.",
    )


def _add_reference_args(parser: argparse.ArgumentParser):
    """
    Add arguments for commands that require references to text.
    """
    parser.add_argument(
        "references",
        nargs="+",
        help="A list of references to summarize (file path, API, web address).",
    )


def _add_query_args(parser: argparse.ArgumentParser):
    """
    Add arguments for commands that require references to text.
    """
    parser.add_argument(
        "query", type=str, help="The query you want to make on some data."
    )


def _add_diff_args(parser: argparse.ArgumentParser):
    """
    Add arguments for the diff command.
    """
    parser.add_argument(
        "diffargs",
        nargs="*",
        help="Contains all of the git diff args.",
    )


def _add_auth_args(parser: argparse.ArgumentParser):
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


def _add_ask_args(parser: argparse.ArgumentParser):
    """
    Add arguments for commands that require references to text.
    """
    parser.add_argument("prompt", type=str, help="Prompt for GPT model.")


def _add_response_args(parser: argparse.ArgumentParser):
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
