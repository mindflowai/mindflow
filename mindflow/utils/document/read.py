from typing import Optional
from mindflow.db.objects.static_definition.document import DocumentType
from mindflow.utils.files.utf8 import is_valid_utf8


def read_document(doc_path: str, doc_type: str) -> Optional[str]:
    """
    Read document
    """
    if doc_type == DocumentType.FILE.value:
        if is_valid_utf8(doc_path):
            with open(doc_path, "r", encoding="utf-8") as file:
                return file.read()
        return None
    else:
        raise Exception(f"Document type {doc_type} not supported")
