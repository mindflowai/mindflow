"""
Module for resolving documents to text.
"""
import sys
from typing import List, Tuple

from mindflow.resolving.resolvers.file_resolver import FileResolver


def resolve(
    document_path: str,
) -> List[Tuple[str, str]]:
    """
    Resolves a document to text.
    """

    resolvers = [FileResolver()]
    for resolver in resolvers:
        if resolver.should_resolve(document_path):
            return resolver.resolve(document_path)

    print(f"Cannot resolve document: {document_path}")
    sys.exit(1)


def resolve_all(document_paths: List[str]) -> List[Tuple[str, str]]:
    document_references: List[Tuple[str, str]] = []
    for document_path in document_paths:
        document_references.extend(resolve(document_path))
    return document_references
