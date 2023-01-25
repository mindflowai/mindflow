"""
Index model
"""

from asyncio import Future
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os

from enum import Enum
from typing import List, Dict, Generator

from mindflow.utils.search_tree import create_text_search_tree
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
        search_tree: dict = None
        size: int = None

        def __init__(self, index_data):
            if index_data is not None:
                self.document_type: str = index_data.get("document_type")
                self.path: str = index_data.get("path")
                self.hash: str = index_data.get("hash")
                self.search_tree: dict = index_data.get("search_tree")
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
            json.dump(self.index, auth_file, indent=4)

    def get_unindexed_documents(self, documents: List[Document]) -> List[Document]:
        """
        Get missing documents from index
        """
        return [document for document in documents if document.hash not in self.index]

    def index_documents(self, documents: List[Document]):
        """
        Create index entries
        """
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Start a separate thread for each document
            future_to_document: List[Future[dict]] = [
                executor.submit(create_text_search_tree, read_document(document))
                for document in documents
            ]

            for future, document in zip(future_to_document, documents):
                document.search_tree = future.result()
                self.save_to_disk([document])
                del document, future

    def get_document_by_hash(
        self, document_hashes: List[str]
    ) -> Generator[List[Document], None, None]:
        """
        Get index document by hash
        """
        # Find all documents with a hash that is in the given list of hashes
        for document_hash in document_hashes:
            if document_hash in self.index:
                yield Index.Document(self.index[document_hash])


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
