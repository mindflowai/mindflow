"""
`refresh` command
"""

import sys
import argparse

from typing import List
from mindflow.client.openai.gpt import GPT

from mindflow.index.generate import generate_index
from mindflow.index.model import index, DocumentReference
from mindflow.utils.args import (
    _add_document_args,
    _add_force_args,
    _add_generate_args,
    _add_remote_args,
)

from mindflow.index.resolve import resolve
from mindflow.utils.helpers import index_type


class Refresh:
    """
    Class for initializing Refresh args and executing the refresh command.
    """

    document_paths: List[str]
    deep_index: bool
    remote: bool
    force: bool

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Refresh all or selected documents in your MindFlow index.",
        )
        _add_document_args(parser)
        _add_generate_args(parser)
        _add_remote_args(parser)
        _add_force_args(parser)

        args = parser.parse_args(sys.argv[2:])

        self.document_paths = args.document_paths
        self.deep_index = args.deep_index
        self.remote = args.remote
        self.force = args.force

    def execute(self):
        """
        This function is used to refresh your MindFlow index.
        """
        GPT.authorize(self.remote)

        if self.remote:
            print("Remote refresh not implemented yet.")
            return

        document_references: List[DocumentReference] = []
        if self.document_paths == ["^"]:
            for document_path in index.document_paths():
                document_references.extend(resolve(document_path))
        else:
            # Resolve documents (Path, URL, etc.) and get their hashes
            for document_path in self.document_paths:
                document_references.extend(resolve(document_path))

        # Generate index and/or embeddings
        kwargs = {
            "remote": self.remote,
            "index_type": index_type(self.deep_index),
            "refresh": True,
            "force": self.force,
        }
        generate_index(document_references, **kwargs)
