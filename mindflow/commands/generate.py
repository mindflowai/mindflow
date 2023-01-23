import sys
import argparse

from typing import List
from mindflow.client.openai.gpt import GPT

from mindflow.index.generate import generate_index
from mindflow.utils.args import (
    _add_document_args,
    _add_remote_args,
)

from mindflow.index.resolve import resolve
from mindflow.index.model import Index


class Generate:
    document_paths: List[str]
    remote: bool

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Generate an index and/or embeddings for files.",
        )
        _add_document_args(parser)
        _add_remote_args(parser)

        args = parser.parse_args(sys.argv[2:])

        self.document_paths = args.document_paths
        self.remote = args.remote

    def execute(self):
        """
        This function is used to generate an index and/or embeddings for files
        """
        if not self.remote:
            GPT.authorize()

        # Resolve documents (Path, URL, etc.)
        documents: List[Index.Document] = []
        for document_path in self.document_paths:
            documents.extend(resolve(document_path))

        # Generate index and/or embeddings
        generate_index(documents, self.remote)
