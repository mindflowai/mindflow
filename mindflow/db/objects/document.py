import hashlib
from typing import Dict, List, Optional
from mindflow.db.controller import DATABASE_CONTROLLER

from mindflow.db.db.database import Collection
from mindflow.db.objects.base import BaseObject
from mindflow.db.objects.model import ConfiguredModel
from mindflow.db.objects.static_definition.document import DocumentType
from mindflow.utils.token import get_token_count


class Document(BaseObject):
    """
    Document
    """

    id: str
    path: str
    document_type: str
    size: int
    hash: str
    search_tree: dict

    _collection = Collection.DOCUMENT
    _database = DATABASE_CONTROLLER.databases.json

    def to_document_reference(
        self,
    ) -> "DocumentReference":
        """
        Create document reference
        """
        return DocumentReference(
            {
                "id": self.id,
                "path": self.path,
                "document_type": self.document_type,
                "hash": self.hash,
            }
        )


class DocumentReference(BaseObject):
    """
    Used to handle referenced to indexed documents or yet uncreated documents.
    """

    id: str
    path: str
    document_type: str

    size: int
    hash: Optional[str]
    new_hash: str
    tokens: int

    def to_document(
        self,
    ) -> Document:
        """
        Create document
        """
        return Document(
            {
                "id": self.id,
                "path": self.path,
                "document_type": self.document_type,
                "size": self.size,
                "hash": self.new_hash,
            }
        )

    @classmethod
    def from_resolved(
        cls, resolved: List[Dict], model: ConfiguredModel
    ) -> List["DocumentReference"]:
        """
        Create document reference from resolved
        """
        document_references: List[DocumentReference] = []
        for resolved_ref in resolved:
            document_reference = cls(resolved_ref)
            document = Document.load(resolved_ref["path"])
            if document:
                document_reference.hash = document.hash

            document_text: Optional[str] = read_document(
                document_reference.id, document_reference.document_type
            )
            if not document_text:
                ## print(f"Unable to read document text: {document_reference.id}")
                continue

            document_text_bytes = document_text.encode("utf-8")

            document_reference.new_hash = hashlib.sha256(
                document_text_bytes
            ).hexdigest()
            document_reference.size = len(document_text_bytes)
            document_reference.tokens = get_token_count(model, document_text)

            document_references.append(document_reference)

        return document_references

    def is_new(self) -> bool:
        """
        Check if document is new
        """
        if not hasattr(self, "hash") or not self.hash:
            return True
        return self.hash != self.new_hash


def read_file_supported_encodings(path: str, supported_encodings=["utf-8", "us-ascii"]):
    # check if file is readable
    for encoding in supported_encodings:
        try:
            text = open(path, "r", encoding=encoding).read()
        except UnicodeDecodeError:
            continue

        return text

    return None


def read_document(document_path: str, document_type: str) -> Optional[str]:
    """
    Read a document.
    """
    if document_type == DocumentType.FILE.value:
        return read_file_supported_encodings(document_path)
    return None
