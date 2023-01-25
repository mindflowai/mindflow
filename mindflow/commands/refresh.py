"""
`refresh` command
"""

import sys
import argparse

from typing import List
from mindflow.client.openai.gpt import GPT

from mindflow.index.generate import generate_index
from mindflow.index.model import index
from mindflow.utils.args import (
    _add_document_args,
    _add_generate_args,
    _add_remote_args,
)

from mindflow.index.resolve import resolve
from mindflow.index.model import Index
from mindflow.utils.config import config as CONFIG


class Refresh:
    """
    Class for initializing Refresh args and executing the refresh command.
    """

    document_paths: List[str]
    deep_index: bool
    remote: bool

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Refresh all or selected documents in your MindFlow index.",
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
        This function is used to refresh your MindFlow index.
        """
        GPT.authorize(self.remote)
        CONFIG.set_deep_index(self.deep_index)

        if self.remote:
            print("Remote refresh not implemented yet.")
            return

        existing_documents: List[Index.Document] = []
        if self.document_paths == ["^"]:
            for document_path in index.get_all_document_paths():
                existing_documents.extend(resolve(document_path))
            index.delete_index()
        else:
            # Resolve documents (Path, URL, etc.) and get their hashes
            documents: List[Index.Document] = []
            for document_path in self.document_paths:
                documents.extend(resolve(document_path))
            existing_documents = list(
                index.get_document_by_hash([document.hash for document in documents])
            )
            index.delete_index_by_hash(
                [existing_document.hash for existing_document in existing_documents]
            )

        if not existing_documents:
            print("Index is empty or no documents specified found in index.")
            return

        # Generate index and/or embeddings
        generate_index(existing_documents, self.deep_index, self.remote)
