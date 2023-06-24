import hashlib
from typing import List, Optional, Union
from mindflow.core.errors import ModelError
from mindflow.core.types.model import ConfiguredModel

from mindflow.core.types.store_traits.pinecone import PineconeStore
from mindflow.core.types.definitions.document import DocumentType


class DocumentReference:
    path: str
    document_type: str

    def __init__(self, path: str, document_type: DocumentType):
        self.path = path
        self.document_type = document_type.value


class Document(PineconeStore):
    # "{hash}"
    id: str
    embedding: list
    path: str
    document_type: str
    num_chunks: int
    size: int
    tokens: int


class DocumentChunk(PineconeStore):
    # ("{hash}_{chunk_id}"
    id: str
    embedding: list
    summary: str
    start_pos: int
    end_pos: int
    tokens = Optional[int]


def read_file_supported_encodings(path: str, supported_encodings=["utf-8", "us-ascii"]):
    for encoding in supported_encodings:
        try:
            text = open(path, "r", encoding=encoding).read()
        except UnicodeDecodeError:
            continue

        return text
    return None


def read_document(path: str, document_type: str) -> Optional[str]:
    if document_type == DocumentType.FILE.value:
        return read_file_supported_encodings(path)
    return None


def get_document_id(path: str, document_type: str) -> Optional[str]:
    if (text := read_document(path, document_type)) is None:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_document_chunk_ids(documents: Union[List[Document], Document]):
    if isinstance(documents, Document):
        documents = [documents]

    total_chunks = sum([document.num_chunks + 1 for document in documents])
    document_chunk_ids = [""] * int(total_chunks)
    j = 0
    for document in documents:
        for i in range(0, int(document.num_chunks) + 1):
            document_chunk_ids[j] = f"{document.id}_{str(i)}"
            j += 1

    return document_chunk_ids
