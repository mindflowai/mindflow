"""
`delete` command
"""

from mindflow.db.objects.document import Document
from mindflow.state import STATE


def delete():
    """
    This function is used to delete your MindFlow index.
    """
    Document.delete_bulk([
        document_reference.path for document_reference in STATE.document_references
    ])
