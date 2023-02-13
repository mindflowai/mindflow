"""
`delete` command
"""

from mindflow.state import STATE
from mindflow.db.db import DATABASE
from mindflow.db.static_definition import Collection


def delete():
    """
    This function is used to delete your MindFlow index.
    """

    paths = [
        document_reference.path for document_reference in STATE.document_references
    ]
    DATABASE.json.delete_object_bulk(Collection.DOCUMENT.value, paths)
