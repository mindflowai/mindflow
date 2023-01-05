"""
File/Directory Resolver
"""
import hashlib
import os
import subprocess

import chardet

from mindflow.resolve.resolvers.base_resolver import BaseResolver, Resolved
from mindflow.utils.reference import Reference

class ResolvedPath(Resolved):
    """
    Reference to a file or directory.
    """
    def __init__(self, path: str):
        self.path = path
        self.type = "file"

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
        text_bytes = open(self.path, "rb").read()
        file_hash = hashlib.sha256(text_bytes).hexdigest()

        return Reference(
            file_hash,
            text_bytes.decode(),
            self.size_bytes,
            self.type,
            self.path,
        )

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

            def criteria(file):
                try:
                    return chardet.detect(open(file, "rb").read())["encoding"] in [
                        "utf-8",
                        "ascii",
                    ]
                except:
                    return False

            return list(filter(criteria, git_files))
                
                
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
