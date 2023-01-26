"""
File/Directory Resolver
"""
import os

from typing import List, Union

from mindflow.index.resolvers.base_resolver import BaseResolver
from mindflow.index.model import DocumentReference

from mindflow.utils.files.utf8 import is_valid_utf8
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

    @staticmethod
    def resolve(document_path: Union[str, os.PathLike]) -> List[DocumentReference]:
        """
        Extract text from files.
        """
        return [
            DocumentReference.initialize(path, "file")
            for path in extract_files(document_path)
            if is_valid_utf8(path)
        ]
