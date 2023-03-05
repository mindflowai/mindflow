"""
`delete` command
"""

from typing import List
from mindflow.db.objects.document import Document
from mindflow.resolving.resolve import resolve_all

def delete(document_paths: List[str]):
    """
    This function is used to delete your MindFlow index.
    """
    Document.delete_bulk([
        document_reference.path for document_reference in resolve_all(document_paths)
    ])
