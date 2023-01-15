"""
Class for references to be sent to backend.
"""

import os


class Reference:
    """
    Reference Class.
    """

    def __init__(
        self,
        reference_hash: str,
        text: str,
        size: int,
        reference_type: str,
        path: os.PathLike,
    ):
        self.hash: str = reference_hash
        self.text: str = text
        self.size: int = size
        self.type: str = reference_type
        self.path: os.PathLike = path
