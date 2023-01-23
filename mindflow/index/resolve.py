"""
Module for resolving documents to text.
"""

from typing import List
from mindflow.index.resolvers.file_resolver import FileResolver
from mindflow.index.model import Index


def resolve(document_path: str) -> List[Index.Document]:
    """
    Resolves a document to text.
    """

    resolvers = [FileResolver()]
    for resolver in resolvers:
        if resolver.should_resolve(document_path):
            return resolver.resolve(document_path)

    raise ValueError(f"Cannot resolve document: {document_path}")
