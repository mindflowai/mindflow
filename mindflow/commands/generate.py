import sys
import argparse

from typing import List
from mindflow.clients.gpt.openai import GPT

from mindflow.index.generate import generate_index
from mindflow.utils.args import (
    _add_reference_args,
    _add_remote_args,
)

from mindflow.index.resolvers.base_resolver import Resolved
from mindflow.index.resolve import resolve


class Generate:
    references: List[str]
    remote: bool

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Generate an index and/or embeddings for files.",
        )
        _add_reference_args(parser)
        _add_remote_args(parser)

        args = parser.parse_args(sys.argv[2:])

        self.references = args.references
        self.remote = args.remote

    def execute(self):
        """
        This function is used to generate an index and/or embeddings for files
        """
        if not self.remote:
            GPT.authorize()

        # Resolve references (Path, URL, etc.)
        resolved_references: List[Resolved] = []
        for reference in self.references:
            resolved_references.extend(resolve(reference))

        # Generate index and/or embeddings
        generate_index(resolved_references, self.remote)
