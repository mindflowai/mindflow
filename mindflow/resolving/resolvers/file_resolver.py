"""
File/Directory Resolver
"""
import os

from typing import List, Optional, Union
from mindflow.db.static_definition import ObjectConfig

from mindflow.resolving.resolvers.base_resolver import BaseResolver
from mindflow.db.objects.document import Document, DocumentReference
from mindflow.db.objects.static_definition.document import DocumentType

from mindflow.utils.files.extract import extract_files


class FileResolver(BaseResolver):
    """
    Resolver for file or directory paths to text.
    """

    @staticmethod
    def read_document(document_path: str) -> Optional[str]:
        """
        Read a document.
        """
        try:
            with open(document_path, "r", encoding="utf-8") as file:
                return file.read()
        except UnicodeDecodeError:
            return None

    @staticmethod
    def should_resolve(document_path: Union[str, os.PathLike]) -> bool:
        """
        Check if a path is a file or directory.
        """
        return os.path.isfile(document_path) or os.path.isdir(document_path)

    def resolve(
        self, document_path: str, document_config: ObjectConfig
    ) -> List[DocumentReference]:
        """
        Extract text from files.
        """
        document_references: List[DocumentReference] = []
        for path in extract_files(document_path):
            document_text = self.read_document(path)
            if not document_text:
                continue
            document_references.append(
                Document.create_document_reference(
                    path, document_text, DocumentType.FILE.value, document_config
                )
            )
        return document_references
