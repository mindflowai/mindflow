"""
File/Directory Resolver
"""
import hashlib
import os
import subprocess

from mindflow.resolve_handling.resolvers.base_resolver import BaseResolver, Resolved
from mindflow.utils.reference import Reference


class ResolvedPath(Resolved):
    """
    Reference to a file or directory.
    """

    def __init__(self, path: str):
        self.path = path

    @property
    def type(self) -> str:
        """
        File type.
        """
        return "file"

    @property
    def size_bytes(self) -> str:
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
                text_bytes = file.read()
            file_hash = hashlib.sha256(text_bytes).hexdigest()
            text = text_bytes.decode("utf-8")
            return Reference(
                file_hash,
                text,
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

    def _get_files(self, reference) -> list:
        """
        Get all files in a directory or a single file.
        """
        command = ["git", "ls-files", reference]

        # Execute the git diff command and retrieve the output as a string
        if os.path.isdir(reference):
            # print(subprocess.check_output(command).decode("utf-8").split("\n"))

            git_files = (
                subprocess.check_output(command).decode("utf-8").split("\n")[:-1]
            )

            return git_files

        return [reference]

    def should_resolve(self, reference) -> bool:
        """
        Check if a path is a file or directory.
        """
        return os.path.isfile(reference) or os.path.isdir(reference)

    def resolve(self, reference) -> list[dict[str, Reference]]:
        """
        Extract text from files.
        """
        files = self._get_files(reference)
        return [ResolvedPath(file) for file in files]
