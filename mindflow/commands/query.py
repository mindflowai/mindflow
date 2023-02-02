"""
`query` command
"""

from typing import List
from mindflow.commands.index import index
from mindflow.state import STATE
from mindflow.client.openai.gpt import GPT

from mindflow.index.query import select_content
from mindflow.utils.response import handle_response_text


def query():
    """
    This function is used to ask a custom question about files, folders, and websites.
    """
    # Generate index and/or embeddings
    if STATE.arguments.index:
        index()

    response = GPT.query(
        STATE.arguments.query,
        select_content(),
    )
    handle_response_text(response)
