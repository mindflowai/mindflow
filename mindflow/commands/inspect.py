"""
`inspect` command
"""
import json
from mindflow.db.db import DATABASE
from mindflow.db.static_definition import Collection
from mindflow.state import STATE


def inspect():
    """
    This function is used to inspect your MindFlow index.
    """
    document_paths = [document.path for document in STATE.document_references]
    print(
        json.dumps(
            DATABASE.json.retrieve_object_bulk(
                Collection.DOCUMENT.value, document_paths
            ),
            indent=4,
        )
    )
