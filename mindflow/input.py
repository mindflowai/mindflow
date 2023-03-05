from enum import Enum
from typing import List


class Command(Enum):
    """
    Arguments for MindFlow
    """

    ASK = "ask"
    COMMIT = "commit"
    CONFIG = "config"
    DELETE = "delete"
    DIFF = "diff"
    INDEX = "index"
    INSPECT = "inspect"
    QUERY = "query"
    REFRESH = "refresh"


class Arguments:
    """
    Arguments for the command line client
    """

    document_paths: List[str]
    force: bool
    index: bool
    diff_args: List[str]
    commit_args: List[str]
    query: str
    skip_clipboard: bool

    def __init__(self, params: dict):
        self.document_paths = params.get("document_paths", [])
        self.force = params.get("force", False)
        self.index = params.get("index", False)
        self.diff_args = params.get("diff_args", [])
        self.commit_args = params.get("commit_args", [])
        self.query = params.get("query", "")
        self.skip_clipboard = params.get("skip_clipboard", False)
