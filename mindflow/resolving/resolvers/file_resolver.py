"""
File/Directory Resolver
"""
import os

from typing import List, Optional, Union

from mindflow.resolving.resolvers.base_resolver import BaseResolver
from mindflow.db.objects.document import Document, DocumentReference
from mindflow.db.objects.static_definition.document import DocumentType

from mindflow.utils.files.extract import extract_files


class FileResolver(BaseResolver):
    """
    Resolver for file or directory paths to text.
    """

    @staticmethod
    def should_resolve(document_path: Union[str, os.PathLike]) -> bool:
        """
        Check if a path is a file or directory.
        """
        return os.path.isfile(document_path) or os.path.isdir(document_path)

    def resolve(self, document_path: str) -> List[DocumentReference]:
        """
        Extract text from files.
        """
        document_references: List[DocumentReference] = []
        for path in extract_files(document_path):
            document_reference: Optional[DocumentReference] = None
            document = Document.load(path)

            if document:
                document_reference = document.to_document_reference()
            else:
                document_reference = DocumentReference.from_path(path, DocumentType.FILE)
            
            if document_reference:
                document_references.append(document_reference)
    
        return document_references
