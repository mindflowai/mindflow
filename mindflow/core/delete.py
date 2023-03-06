"""
`delete` command
"""

from typing import List
from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.objects.document import Document
from mindflow.resolving.resolve import resolve_all

def run_delete(document_paths: List[str]):
    """
    This function is used to delete your MindFlow index.
    """
    Document.delete_bulk([
        document_reference.path for document_reference in resolve_all(document_paths)
    ])
    DATABASE_CONTROLLER.databases.json.save_file()