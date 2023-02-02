"""
`delete` command
"""

from mindflow.state import STATE
from mindflow.db.db import delete_object_bulk


def delete():
    """
    This function is used to delete your MindFlow index.
    """

    paths = [
        document_reference.path for document_reference in STATE.document_references
    ]
    delete_object_bulk(paths, STATE.db_config.document)
