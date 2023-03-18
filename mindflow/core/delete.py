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
    resolved_paths = [
        resolved_path["path"] for resolved_path in resolve_all(document_paths)
    ]
    documents_to_delete = [
        document.path if document else None
        for document in Document.load_bulk(resolved_paths)
    ]

    if len(documents_to_delete) == 0:
        return "No documents to delete"

    Document.delete_bulk(documents_to_delete)

    DATABASE_CONTROLLER.databases.json.save_file()
    return "Documents deleted"
