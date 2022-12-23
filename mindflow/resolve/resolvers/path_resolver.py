"""
File/Directory Resolver
"""
import hashlib
import os
import subprocess

import chardet

from mindflow.resolve.resolvers.base_resolver import BaseResolver
from mindflow.utils.reference import Reference

MAX_LENGTH = 10_000
FILES_RETURNED_IF_OVER_MAX = 5
SLEEP_SECONDS = 5


def preprocess_file_text(text):
    return text.strip().replace("\n", " ").replace("\t", " ")


class PathResolver(BaseResolver):
    """
    Resolver for file or directory paths to text.
    """

    def __init__(self, reference):
        self.reference = reference

    def _get_files(self) -> list:
        """
        Get all files in a directory or a single file.
        """
        command = ["git", "ls-files", self.reference]

        # Execute the git diff command and retrieve the output as a string
        if os.path.isdir(self.reference):
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
                
                
        return [self.reference]
    
    def _get_resolved_file(self, file: str) -> dict[str, Reference]:
        file_bytes = open(file, "rb").read()
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        return {file_hash: Reference(file_hash, file_bytes, "path", file)}
    

    def should_resolve(self) -> bool:
        """
        Check if a path is a file or directory.
        """
        return os.path.isfile(self.reference) or os.path.isdir(self.reference)

    
    def resolve(self) -> list[dict[str, Reference]]:
        """
        Extract text from files.
        """
        resolved_files = {}
        [resolved_files.update(self._get_resolved_file(file)) for file in self._get_files()]
        return resolved_files
    

