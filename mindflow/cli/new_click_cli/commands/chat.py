"""
`ask` command
"""
import click
from typing import Tuple
import os

from mindflow.core.chat import run_chat
from mindflow.core.index import run_index
from mindflow.core.query import run_query
from mindflow.core.search.chat_agency import run_agent_query, Conversation


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


@click.command(
    help='Interact with ChatGPT, you can reference files and directories by passing them as arguments. Example: `mf chat "Please summarize this file" path/to/file.txt`'
)
@click.option("-s", "--skip-index", type=bool, default=False, is_flag=True)
@click.argument("prompt_args", nargs=-1, type=str, required=True)
def chat(prompt_args: Tuple[str], skip_index: bool):
    prompt, paths = _parse_chat_prompt_args(prompt_args)

    # if paths:

    has_dirs = False
    for path in paths:
        if os.path.isdir(path):
            has_dirs = True
            break

    if has_dirs:
        if skip_index:
            click.echo(
                "Skipping indexing step, only using the current index for context. You can run `mf index` to pre-index specific paths."
            )
        else:
            click.echo(
                "Indexing paths... Note: this may take a while, if you want to skip this step, use the `--skip-index` flag. If you do so, you can pre-select specific paths to index with `mf index`.\n"
            )

            run_index(paths, refresh=False, verbose=False)
            click.echo("")
        print(run_query(paths, prompt))
    else:
        print(run_agent_query(paths, prompt))


@click.group(help="Manage conversation histories.")
def history():
    pass


@history.command(help="View chat history stats.")
def stats():
    convo = Conversation(conversation_id=0)
    print("Num messages:", len(convo.messages))
    print("Total tokens:", convo.total_tokens)


@history.command(help="Clear the chat history.")
def clear():
    convo = Conversation(conversation_id=0)
    convo.clear()
    convo.save()
