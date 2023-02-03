"""
`inspect` command
"""
import json
from mindflow.db.db import retrieve_object_bulk
from mindflow.state import STATE


def inspect():
    """
    This function is used to inspect your MindFlow index.
    """
    document_paths = [document.path for document in STATE.document_references]
    print(
        json.dumps(
            retrieve_object_bulk(document_paths, STATE.db_config.document), indent=4
        )
    )
