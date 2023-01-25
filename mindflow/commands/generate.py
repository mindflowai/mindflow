"""
`generate` command
"""

import sys
import argparse

from typing import List
from mindflow.client.openai.gpt import GPT

from mindflow.index.generate import generate_index
from mindflow.utils.args import (
    _add_document_args,
    _add_generate_args,
    _add_remote_args,
)
from mindflow.utils.config import config as CONFIG

from mindflow.index.resolve import resolve
from mindflow.index.model import Index


class Generate:
    """
    Class for initializing Generate args and executing the generate command.
    """

    document_paths: List[str]
    deep_index: bool
    remote: bool

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Generate an index and/or embeddings for files.",
        )
        _add_document_args(parser)
        _add_generate_args(parser)
        _add_remote_args(parser)

        args = parser.parse_args(sys.argv[2:])

        self.document_paths = args.document_paths
        self.deep_index = args.deep_index
        self.remote = args.remote

    def execute(self):
        """
        This function is used to generate an index and/or embeddings for files
        """
        GPT.authorize(self.remote)
        CONFIG.set_deep_index(self.deep_index)

        # Resolve documents (Path, URL, etc.)
        documents: List[Index.Document] = []
        for document_path in self.document_paths:
            documents.extend(resolve(document_path))

        # Generate index and/or embeddings
        generate_index(documents, self.remote)
