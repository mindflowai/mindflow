"""
Index model
"""

from asyncio import Future
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os

from enum import Enum
from typing import List, Dict

from mindflow.client.openai.gpt import GPT
from mindflow.utils.config import config as Config
from mindflow import DOT_MINDFLOW

INDEX_PATH = os.path.join(DOT_MINDFLOW, "index.json")


class DocumentType(Enum):
    """
    Document type enum
    """

    FILE: str = "file"


class Index:
    """
    Index model
    """

    class Document:
        """
        Document
        """

        document_type: str = None
        path: str = None
        hash: str = None
        embedding: List[float] = None
        size: int = None

        def __init__(self, index_data):
            if index_data is not None:
                self.document_type: str = index_data.get("document_type")
                self.path: str = index_data.get("path")
                self.hash: str = index_data.get("hash")
                self.embedding: List[float] = index_data.get("embedding")
                self.size: int = index_data.get("size")

        @classmethod
        def initialize(cls, document_type: str, path: str) -> "Index.Document":
            """
            Create document
            """
            document = cls(None)
            document.document_type = document_type
            document.path = path

            text_bytes = read_document(document).encode()
            document.size = len(text_bytes)
            document.hash = hashlib.sha256(text_bytes).hexdigest()
            return document

    index: Dict[str, Document]

    def __init__(self):
        self.index = self.load_from_disk()

    def load_from_disk(self) -> dict:
        """
        Load index from disk (JSON)
        """
        if os.path.isfile(INDEX_PATH):

            # Open the authentication file in read and write mode
            with open(INDEX_PATH, "r+", encoding="utf-8") as index_file:
                # Read the existing authentication data
                return json.load(index_file)
        else:
            return {}

    def save_to_disk(self, documents: List[Document]):
        """
        Add index to disk (JSON)
        """
        update = {document.hash: vars(document) for document in documents}
        self.index.update(update)
        with open(INDEX_PATH, "w", encoding="utf-8") as auth_file:
            json.dump(self.index, auth_file)

    def get_unindexed_documents(self, documents: List[Document]) -> List[str]:
        """
        Get missing documents from index
        """
        return [document for document in documents if document.hash not in self.index]

    def index_documents(self, documents: List[Document]):
        """
        Create index entries
        """
        documents_w_embeddings = [None] * len(documents)
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Start a separate thread for each document
            future_to_document: dict[Future[Index], Index.Document] = {
                executor.submit(self._embed_document, document): document
                for document in documents
            }

            # Wait for all threads to complete
            count = 0
            for future in as_completed(future_to_document):
                try:
                    document: "Index.Document" = future.result()
                except Exception as error:
                    print(f"Error creating document {error}")
                else:
                    # Remove anti-pattern
                    documents_w_embeddings[count] = document
                    count += 1
        if len(documents_w_embeddings) != 0:
            documents_w_embeddings = [
                document for document in documents_w_embeddings if document is not None
            ]
            self.save_to_disk(documents_w_embeddings)

    def get_document_by_hash(self, hashes: List[str]) -> List["Index"]:
        """
        Get index document by hash
        """
        # Find all documents with a hash that is in the given list of hashes
        entries: dict = [self.index[hash] for hash in hashes if hash in self.index]
        # Return a list of cls objects constructed from the found documents
        return [Index.Document(index) for index in entries]

    @staticmethod
    def _embed_document(document: Document) -> Document:
        """
        Create index document
        """
        document.embedding = GPT.get_embedding(
            read_document(document), Config.GPT_MODEL_EMBEDDING
        )
        return document


def read_document(document: Index.Document) -> str:
    """
    Read document
    """
    if document.document_type == "file":
        with open(document.path, "r", encoding="utf-8") as file:
            return file.read()
    else:
        raise Exception(f"Document type {document.document_type} not supported")


index = Index()
