"""
File/Directory Resolver
"""
import hashlib
import logging
import os
import codecs

from typing import List, Union

from mindflow.resolve_handling.resolvers.base_resolver import BaseResolver, Resolved
from mindflow.utils.reference import Reference
from mindflow.utils.git import is_within_git_repo, get_git_files


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

    def extract_files(self, path: os.PathLike) -> List[os.PathLike]:
        """
        Extract all files from a directory.
        """
        file_paths = []
        if os.path.isfile(path):
            return [os.fspath(path)]
        if is_within_git_repo(path):
            return get_git_files(path)
        try:
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_file():
                        file_paths.append(os.fspath(entry.path))
                    elif entry.is_dir():
                        file_paths.extend(self.extract_files(entry.path))
            return file_paths
        except IsADirectoryError as error:
            logging.debug("Could not read directory/file: %s", path)
            logging.debug(error)
            return file_paths

    def is_valid_utf8(self, file_path: os.PathLike) -> bool:
        """
        Check if a file is valid utf8.
        """
        try:
            for _ in codecs.open(file_path, encoding="utf-8", errors="strict"):
                pass
            return True
        except UnicodeDecodeError:
            return False

    def should_resolve(self, reference: Union[str, os.PathLike]) -> bool:
        """
        Check if a path is a file or directory.
        """
        return os.path.isfile(reference) or os.path.isdir(reference)

    def resolve(self, reference: Union[str, os.PathLike]) -> List[ResolvedPath]:
        """
        Extract text from files.
        """
        return [ResolvedPath(file) for file in self.extract_files(reference) if self.is_valid_utf8(file)]