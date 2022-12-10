"""
File/Directory Resolver
"""
import os

import chardet

from mindflow.resolve.resolvers.base_resolver import BaseResolver


class PathResolver(BaseResolver):
    """
    Resolver for file or directory paths to text.
    """

    def __init__(self, reference):
        self.reference = reference
        self.files = self._get_files()

    def _get_files(self) -> list:
        """
        Get all files in a directory or a single file.
        """
        if os.path.isdir(self.reference):
            return [
                os.path.join(root, file)
                for root, dirs, files in os.walk(self.reference)
                for file in files
                if chardet.detect(open(os.path.join(root, file), "rb").read())[
                    "encoding"
                ]
                in ["utf-8", "ascii"]
            ]
        return [self.reference]

    def should_resolve(self) -> bool:
        """
        Check if a path is a file or directory.
        """
        return os.path.isfile(self.reference) or os.path.isdir(self.reference)

    def resolve(self) -> dict:
        """
        Extract text from files.
        """
        return {
            file: {
                "text": open(file, encoding="utf-8", errors="ignore")
                .read()
                .strip()
                .replace("\n", " "),
                "type": "path",
            }
            for file in self.files
        }
