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
    document_to_delete = [document_reference.path for document_reference in resolve_all(document_paths)]
    
    Document.delete_bulk(document_to_delete)
    
    DATABASE_CONTROLLER.databases.json.save_file()
    return "Documents deleted"