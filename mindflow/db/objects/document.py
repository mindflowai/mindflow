import hashlib
from typing import Optional, Union
from mindflow.db.static_definition import ObjectConfig
from mindflow.db.db import retrieve_object


class Document:
    """
    Document
    """

    id: str
    path: str
    document_type: str
    hash: str
    size: int
    search_tree: dict

    def __init__(self, params: Union[dict, None]):
        if params is None:
            return
        self.id = params.get("id", params.get("path", None))
        self.path = params.get("path", None)
        self.document_type = params.get("document_type", None)
        self.hash = params.get("hash", None)
        self.size = params.get("size", None)
        self.search_tree = params.get("search_tree", None)

    @classmethod
    def create_document_reference(
        cls,
        document_path: str,
        document_text: str,
        document_type: str,
        document_config: ObjectConfig,
    ) -> Optional["DocumentReference"]:
        """
        Create document reference
        """
        document = cls(retrieve_object(document_path, document_config))
        old_hash = None
        if hasattr(document, "hash"):
            old_hash = document.hash

        document_text_bytes = document_text.encode("utf-8")
        return DocumentReference(
            id=document_path,
            path=document_path,
            document_type=document_type,
            size=len(document_text_bytes),
            hash=hashlib.sha256(document_text_bytes).hexdigest(),
            old_hash=old_hash,
        )


class DocumentReference:
    """
    Used to handle referenced to indexed documents or yet uncreated documents.
    """

    id: str
    path: str
    document_type: str
    size: int
    hash: str
    old_hash: Optional[str]

    def __init__(
        self,
        id: str,
        path: str,
        document_type: str,
        size: int,
        hash: str,
        old_hash: Optional[str],
    ):
        self.id = id
        self.path = path
        self.document_type = document_type
        self.size = size
        self.hash = hash
        self.old_hash = old_hash
