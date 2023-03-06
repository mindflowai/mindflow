"""
Module for resolving documents to text.
"""

import sys
from typing import List, Optional

from mindflow.db.objects.document import DocumentReference
from mindflow.input import Command
from mindflow.resolving.resolvers.file_resolver import FileResolver


def resolve(document_path: str) -> List[DocumentReference]:
    """
    Resolves a document to text.
    """

    resolvers = [FileResolver()]
    for resolver in resolvers:
        if resolver.should_resolve(document_path):
            return resolver.resolve(document_path)

    print(f"Cannot resolve document: {document_path}")
    sys.exit(1)

def resolve_all(document_paths: List[str]) -> List[DocumentReference]:
    document_references: List[DocumentReference] = []
    for document_path in document_paths:
        document_references.extend(resolve(document_path))
    return document_references

def return_if_indexable(document_references: List[DocumentReference], refresh: bool, force: bool) -> List[DocumentReference]:
    return [
        document_reference
        for document_reference in document_references
        if index_document(document_reference, refresh, force)
    ]

def index_document(
    document_reference: DocumentReference, refresh: bool, force: Optional[bool]
) -> bool:
    if refresh:
        if not document_reference.old_hash:
            return False
        if document_reference.old_hash == document_reference.hash and not force:
            return False
        return True
  
    if not hasattr(document_reference, "old_hash") or force:
        return True
    return False
