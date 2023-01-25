"""
`delete` command
"""

import sys
import argparse

from typing import List
from mindflow.index.model import Index, index
from mindflow.index.resolve import resolve

from mindflow.utils.args import (
    _add_document_args,
    _add_remote_args,
)


class Delete:
    """
    Class for initializing Delete args and executing the delete command.
    """

    document_paths: List[str]
    remote: bool

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Delete your MindFlow index.",
        )
        _add_document_args(parser)
        _add_remote_args(parser)

        args = parser.parse_args(sys.argv[2:])

        self.document_paths = args.document_paths
        self.remote = args.remote

    def execute(self):
        """
        This function is used to delete your MindFlow index.
        """
        if self.remote:
            print("Remote delete not implemented yet.")
            return

        if self.document_paths == ["^"]:
            index.delete_index()
        else:
            # Resolve documents (Path, URL, etc.) and get their hashes
            documents: List[Index.Document] = [
                resolve(document_path) for document_path in self.document_paths
            ]
            index.delete_index_by_hash([document.hash for document in documents])
