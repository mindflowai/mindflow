"""
File/Directory Resolver
"""
import hashlib
import os

from typing import List, Union

from mindflow.resolve_handling.resolvers.base_resolver import BaseResolver, Resolved
from mindflow.utils.reference import Reference
from mindflow.utils.files.utf8 import is_valid_utf8
from mindflow.utils.files.extract import extract_files


class ResolvedPath(Resolved):
    """
    Reference to a file or directory.
    """

    def __init__(self, path: os.PathLike):
        self.path = os.fspath(path)

    @property
    def type(self) -> str:
        """
        File type.
        """
        return "file"

    @property
    def size_bytes(self) -> int:
        """
        File size in bytes.
        """
        return os.stat(self.path).st_size

    @property
    def text_hash(self) -> str:
        """
        File hash.
        """
        return hashlib.sha256(open(self.path, "rb").read()).hexdigest()

    def create_reference(self) -> Reference:
        """
        Create a reference to a file or directory.
        """
        try:
            with open(self.path, "rb") as file:
                text_bytes: bytes = file.read()
            return Reference(
                hashlib.sha256(text_bytes).hexdigest(),
                text_bytes.decode("utf-8"),
                self.size_bytes,
                self.type,
                self.path,
            )
        except UnicodeDecodeError:
            return None

class PathResolver(BaseResolver):
    """
    Resolver for file or directory paths to text.
    """
    @staticmethod
    def should_resolve(reference: Union[str, os.PathLike]) -> bool:
        """
        Check if a path is a file or directory.
        """
        return os.path.isfile(reference) or os.path.isdir(reference)

    @staticmethod
    def resolve(reference: Union[str, os.PathLike]) -> List[ResolvedPath]:
        """
        Extract text from files.
        """
        return [ResolvedPath(file) for file in extract_files(reference) if is_valid_utf8(file)]
