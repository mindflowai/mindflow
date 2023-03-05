import hashlib
from typing import Optional
from mindflow.db.db.database import Collection
from mindflow.db.objects.base import BaseObject
from mindflow.db.objects.static_definition.document import DocumentType


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

    def to_document_reference(
        self,
    ) -> "DocumentReference":
        """
        Create document reference
        """
        document_text: Optional[str] = read_document(self.id, self.document_type)
        if not document_text:
            raise Exception("Document text not found")
        
        document_text_bytes = document_text.encode("utf-8")
        return DocumentReference(
            {
                "id": self.id,
                "path": self.path,
                "document_type": self.document_type,
                "size": len(document_text_bytes),
                "hash": hashlib.sha256(document_text_bytes).hexdigest(),
                "old_hash": self.hash,
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
    hash: str
    old_hash: Optional[str]

    def to_document(
        self,
    ) -> Document:
        """
        Create document
        """
        return Document({
            "id": self.id,
            "path": self.path,
            "document_type": self.document_type,
            "size": self.size,
            "hash": self.hash,
        })

    @classmethod
    def from_path(
        cls,
        document_path: str,
        document_type: DocumentType,
    ) -> Optional["DocumentReference"]:
        """
        Create document reference from path
        """
        document_text: Optional[str] = read_document(document_path, document_type.value)
        if not document_text:
            return None
        document_text_bytes = document_text.encode()
        return cls({
            "id": document_path,
            "path": document_path,
            "document_type": document_type.value,
            "size": len(document_text_bytes),
            "hash": hashlib.sha256(document_text_bytes).hexdigest(),
        })

def read_document(document_path: str, document_type: str) -> Optional[str]:
    """
    Read a document.
    """
    match document_type:
        case DocumentType.FILE.value:
            try:
                with open(document_path, "r", encoding="utf-8") as file:
                    return file.read()
            except UnicodeDecodeError:
                return None
        case _:
            return None