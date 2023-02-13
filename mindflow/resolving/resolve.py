"""
Module for resolving documents to text.
"""

from typing import List

from mindflow.db.objects.document import DocumentReference
from mindflow.resolving.resolvers.file_resolver import FileResolver


def resolve(document_path: str) -> List[DocumentReference]:
    """
    Resolves a document to text.
    """

    resolvers = [FileResolver()]
    for resolver in resolvers:
        if resolver.should_resolve(document_path):
            return resolver.resolve(document_path)

    raise ValueError(f"Cannot resolve document: {document_path}")
