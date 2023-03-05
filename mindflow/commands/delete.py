"""
`delete` command
"""

from mindflow.db.objects.document import Document
from mindflow.state import STATE


def delete():
    """
    This function is used to delete your MindFlow index.
    """

    paths = [
        document_reference.path for document_reference in STATE.document_references
    ]
    Document.delete_bulk(paths)
