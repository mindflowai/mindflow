"""
`query` command
"""

import argparse

import sys

from typing import List

from mindflow.client.openai.gpt import GPT
from mindflow.client.mindflow.query import query as remote_query

from mindflow.utils.response import handle_response_text
from mindflow.index.generate import generate_index
from mindflow.index.resolve import resolve
from mindflow.index.model import Index
from mindflow.utils.args import (
    _add_query_args,
    _add_generate_args,
    _add_document_args,
    _add_remote_args,
    _add_response_args,
)
from mindflow.command_helpers.query.query import query as local_query


class Query:
    """
    Class for initializing Query args and executing the query command.
    """

    query: str
    document_paths: List[str]
    index: bool
    remote: bool
    return_prompt: bool
    skip_clipboard: bool

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="This command is use to query files, folders, and websites.",
        )
        _add_query_args(parser)
        _add_document_args(parser)
        _add_generate_args(parser)
        _add_response_args(parser)
        _add_remote_args(parser)

        args = parser.parse_args(sys.argv[2:])

        self.document_paths = args.document_paths
        self.index = args.index
        self.remote = args.remote
        self.query = args.query
        self.return_prompt = args.return_prompt
        self.skip_clipboard = args.skip_clipboard

    def execute(self):
        """
        This function is used to ask a custom question about files, folders, and websites.
        """
        GPT.authorize(self.remote)

        # Resolve documents (Path, URL, etc.)
        documents: List[Index.Document] = []
        for document_path in self.document_paths:
            documents.extend(resolve(document_path))

        # Generate index and/or embeddings
        if self.index:
            generate_index(documents, self.remote)

        # Query through Mindflow API or locally
        if self.remote:
            response: str = remote_query(self.query, documents, self.return_prompt).text
        else:
            response: str = local_query(self.query, documents, self.return_prompt)

        handle_response_text(response, self.skip_clipboard)
