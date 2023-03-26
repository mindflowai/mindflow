import hashlib
from typing import List, Optional

import numpy as np
from mindflow.db.controller import DATABASE_CONTROLLER

from mindflow.db.db.database import Collection
from mindflow.db.objects.base import BaseObject
from mindflow.db.objects.static_definition.document import DocumentType


class Document(BaseObject):
    """
    Document
    """

    # "{hash}"
    id: str
    embedding: Optional[np.ndarray]
    path: str
    document_type: str
    num_chunks: Optional[int]
    size: int
    tokens: int

    _collection = Collection.DOCUMENT
    _database = DATABASE_CONTROLLER.databases.pinecone


class DocumentChunk(BaseObject):
    """
    Document chunk
    """

    # ("{hash}_{chunk_id}"
    id: str
    embedding: np.ndarray
    summary: str
    start_pos: int
    end_pos: int
    tokens = Optional[int]

    _collection = Collection.DOCUMENT_CHUNK
    _database = DATABASE_CONTROLLER.databases.pinecone

    @classmethod
    def query(
        cls, vector: np.ndarray, ids: List[str], top_k=100, include_metadata=True
    ):
        return [
            cls(chunk)
            for chunk in cls._database.query(
                cls._collection.value, vector, ids, top_k, include_metadata
            )
        ]


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


def get_document_id(document_path: str, document_type: str) -> str:
    """
    This function is used to generate a document id.
    """
    text = read_document(document_path, document_type)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
