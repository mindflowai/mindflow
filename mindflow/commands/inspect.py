"""
`inspect` command
"""
import json
from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.db.database import Collection
from mindflow.state import STATE


def inspect():
    """
    This function is used to inspect your MindFlow index.
    """
    document_paths = [document.path for document in STATE.document_references]
    print(
        json.dumps(
            DATABASE_CONTROLLER.databases.json.load_bulk(
                Collection.DOCUMENT.value, document_paths
            ),
            indent=4,
        )
    )
