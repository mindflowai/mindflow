"""
`ask` command
"""
import click
from typing import Tuple
import os

from mindflow.core.chat import run_chat
from mindflow.core.index import run_index
from mindflow.core.query import run_query


def _parse_chat_prompt_args(prompt_args: Tuple[str]):
    # takes a list of strings and returns a string along with any filenames/directories that were passed.
    # note: if the user passes a string that contains a bunch of text, with a filename/directory in the middle,
    # those filenames/directories will be ignored and treated as plain text.

    prompt = " ".join(prompt_args)  # include files/directories in prompt
    paths = []

    for arg in prompt_args:
        # check if valid path string
        if os.path.exists(arg):
            paths.append(arg)

    return prompt, paths


@click.command(help="Interact with ChatGPT, you can reference files and directories by passing them as arguments. Example: `mf chat \"Please summarize this file\" path/to/file.txt`")
@click.option("-i", "--ignore-paths", type=bool, default=False, is_flag=True)
@click.argument("prompt_args", nargs=-1, type=str, required=True)
def chat(prompt_args: Tuple[str], ignore_paths: bool):
    prompt, paths = _parse_chat_prompt_args(prompt_args)
    if ignore_paths:
        click.echo("Note: the following paths were ignored: " + str(paths))
        paths.clear()

    if paths:
        run_index(paths, refresh=False, verbose=False)
        click.echo("")
        print(run_query(paths, prompt))
    else:
        print(run_chat(prompt))
