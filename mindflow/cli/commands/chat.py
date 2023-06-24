import asyncio
import click
from typing import Tuple
import os

from result import Result

from mindflow.core.commands.chat import run_chat
from mindflow.core.commands.index import run_index
from mindflow.core.commands.query import run_query
from mindflow.core.settings import Settings
from mindflow.core.types.model import ModelApiCallError
from mindflow.core.types.store_traits.json import save_json_store
from mindflow.core.types.conversation import Conversation
from mindflow.core.types.definitions.conversation import ConversationID


def parse_chat_prompt_and_paths_from_args(prompt_args: Tuple[str]):
    prompt = " ".join(prompt_args)  # include files/directories in prompt
    paths = []

    for arg in prompt_args:
        if os.path.exists(arg):
            paths.append(arg)

    return prompt, paths


@click.command(
    help='Interact with ChatGPT, you can reference files and directories by passing them as arguments. Example: `mf chat "Please summarize this file" path/to/file.txt`'
)
@click.option("-s", "--skip-index", type=bool, default=False, is_flag=True)
@click.argument("prompt_args", nargs=-1, type=str, required=True)
def chat(prompt_args: Tuple[str], skip_index: bool):
    prompt, paths = parse_chat_prompt_and_paths_from_args(prompt_args)
    settings = Settings()
    if paths:
        if skip_index:
            click.echo(
                "Skipping indexing step, only using the current index for context. You can run `mf index` to pre-index specific paths."
            )
        else:
            click.echo(
                "Indexing paths... Note: this may take a while, if you want to skip this step, use the `--skip-index` flag. If you do so, you can pre-select specific paths to index with `mf index`.\n"
            )

            asyncio.run(run_index(settings, paths))

        run_query_result: Result[str, ModelApiCallError] = asyncio.run(
            run_query(settings, paths, prompt)
        )
        click.echo(run_query_result.value)

        save_json_store()
        return

    run_chat_result: Result[str, ModelApiCallError] = asyncio.run(
        run_chat(settings, [], prompt)
    )
    click.echo(run_chat_result.value)
    save_json_store()


@click.group(help="Manage conversation histories.")
def history():
    pass


@history.command(help="View chat history stats.")
def stats():
    if (conversation := Conversation.load(ConversationID.CHAT_0.value)) is None:
        print("No conversation history found.")
        return

    print("Num messages:", len(conversation.messages))
    print("Total tokens:", conversation.total_tokens)


@history.command(help="Clear the chat history.")
def clear():
    if (conversation := Conversation.load(ConversationID.CHAT_0.value)) is None:
        print("No conversation history found.")
        return

    conversation.messages = []
    conversation.save()
