from enum import Enum
from typing import List

from mindflow.db.static_definition import Collection, ObjectConfig, ObjectStoreType

class Command(Enum):
    """
    Arguments for MindFlow
    """

    ASK = "ask"
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
    git_diff_args: List[str]
    query: str
    skip_clipboard: bool

    def __init__(self, params: dict):
        self.document_paths = params.get("document_paths", [])
        self.force = params.get("force", False)
        self.index = params.get("index", False)
        self.git_diff_args = params.get("git_diff_args", [])
        self.query = params.get("query", "")
        self.skip_clipboard = params.get("skip_clipboard", False)


class DBConfig:
    def __init__(self, database: str, path: str):
        self.service = ObjectConfig(
            ObjectStoreType.STATIC.value, Collection.SERVICE.value, None
        )
        self.model = ObjectConfig(
            ObjectStoreType.STATIC.value, Collection.MODEL.value, None
        )
        self.model_config = ObjectConfig(
            database,
            Collection.MODEL_CONFIG.value,
            path,
        )

        self.mindflow_model_config = ObjectConfig(
            database,
            Collection.MINDFLOW_MODEL_CONFIG.value,
            path,
        )

        self.service_config = ObjectConfig(
            database,
            Collection.SERVICE_CONFIG.value,
            path,
        )

        self.document = ObjectConfig(database, Collection.DOCUMENT.value, path)
