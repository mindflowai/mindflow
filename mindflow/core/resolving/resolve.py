"""Module for resolving documents types."""
import sys
from typing import List
from mindflow.core.types.document import DocumentReference

from mindflow.core.resolving.resolvers.file_resolver import FileResolver


def resolve_path_to_document_reference(
    document_path: str,
) -> List[DocumentReference]:
    resolvers = [FileResolver()]
    for resolver in resolvers:
        if resolver.should_resolve(document_path):
            return resolver.resolve_to_document_reference(document_path)

    print(f"Cannot resolve document: {document_path}")
    sys.exit(1)


def resolve_paths_to_document_references(
    document_paths: List[str],
) -> List[DocumentReference]:
    return [
        ref
        for document_path in document_paths
        for ref in resolve_path_to_document_reference(document_path)
    ]
