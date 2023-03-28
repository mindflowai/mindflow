"""
File/Directory Resolver
"""
import os
from typing import List, Tuple, Union

from mindflow.db.objects.static_definition.document import DocumentType
from mindflow.resolving.resolvers.base_resolver import BaseResolver
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
        abs_path = os.path.abspath(document_path)
        return os.path.isfile(abs_path) or os.path.isdir(abs_path)

    def resolve(self, document_path: str) -> List[Tuple[str, str]]:
        """
        Extract text from files.
        """
        return [
            (path, DocumentType.FILE.value)
            for path in extract_files(os.path.abspath(document_path))
        ]
