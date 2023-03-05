"""
`inspect` command
"""
import json
from typing import List
from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.db.database import Collection

def inspect(document_paths: List[str]):
    """
    This function is used to inspect your MindFlow index.
    """
    print(
        json.dumps(
            DATABASE_CONTROLLER.databases.json.load_bulk(
                Collection.DOCUMENT.value, document_paths
            ),
            indent=4,
        )
    )
