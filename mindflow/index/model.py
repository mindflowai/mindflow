"""
Index model
"""

from asyncio import Future
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os

from enum import Enum
from typing import List, Dict, Generator, Union

from mindflow.utils.search_tree import create_text_search_tree
from mindflow.utils.config import config as CONFIG
from mindflow.utils.document.read import read_document


class DocumentReference:
    """
    Used to handle referenced to indexed documents or yet uncreated documents.
    """

    doc_path: str
    doc_type: str
    doc_hash: str
    doc_size: int
    doc_index_type: Union[str, None]
    doc_exists: bool

    def __init__(self, doc_path: str, doc_type: str):
        self.doc_path = doc_path
        self.doc_type = doc_type

    @classmethod
    def initialize(cls, path: str, doc_type: str) -> "DocumentReference":
        """
        Create a document reference from an existing index.
        """
        new_document_reference = cls(path, doc_type).set_meta_data()
        document: Index.Document = None
        try:
            document = next(iter(index.documents(new_document_reference)))
        except StopIteration:
            pass

        if document:
            new_document_reference.doc_index_type = document.index_type
            new_document_reference.doc_exists = True
        return new_document_reference

    def set_meta_data(self) -> "DocumentReference":
        """
        Set the meta data of a document reference.
        """
        doc_text = read_document(self.doc_path, self.doc_type).encode()
        self.doc_hash = hashlib.sha256(doc_text).hexdigest()
        self.doc_size = len(doc_text)
        return self


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
        index_type: str = None
        search_tree: dict = None
        size: int = None

        def __init__(self, index_data):
            if index_data is not None:
                self.document_type: str = index_data.get("document_type")
                self.path: str = index_data.get("path")
                self.hash: str = index_data.get("hash")
                self.index_type: str = index_data.get("index_type")
                self.search_tree: dict = index_data.get("search_tree")
                self.size: int = index_data.get("size")

        @classmethod
        def initialize(cls, document_reference: DocumentReference) -> "Index.Document":
            """
            Create document
            """
            document = cls(None)
            document.path = document_reference.doc_path
            document.document_type = document_reference.doc_type
            document.size = document_reference.doc_size
            document.hash = document_reference.doc_hash
            return document

    index: Dict[str, Document]

    def __init__(self):
        self.index = self.load_from_disk()

    def show(
        self,
        document_references: Union[None, DocumentReference, List[DocumentReference]],
    ) -> str:
        """
        Show documents without embeddings
        """

        def prune_embeddings(tree):
            if "embedding" in tree:
                del tree["embedding"]
            if tree["leaves"] is not None:
                for leaf in tree["leaves"]:
                    prune_embeddings(leaf)

        if document_references is None:
            for document in self.documents(self.index.keys()):
                prune_embeddings(document.search_tree)
                print(json.dumps(vars(document), indent=4))
        for document in self.documents(document_references):
            prune_embeddings(document.search_tree)
            print(json.dumps(vars(document), indent=4))

    def save_to_disk(self, documents: List[Document]):
        """
        Add index to disk (JSON)
        """
        update = {document.path: vars(document) for document in documents}
        self.index.update(update)
        with open(CONFIG.INDEX_PATH, "w", encoding="utf-8") as disk_file:
            json.dump(self.index, disk_file, indent=4)

    def load_from_disk(self) -> dict:
        """
        Load index from disk (JSON)
        """
        if os.path.isfile(CONFIG.INDEX_PATH):

            # Open the authentication file in read and write mode
            with open(CONFIG.INDEX_PATH, "r+", encoding="utf-8") as index_file:
                # Read the existing authentication data
                return json.load(index_file)
        else:
            return {}

    def delete_documents(
        self,
        document_references: Union[None, DocumentReference, List[DocumentReference]],
    ):
        """
        Remove documents from index
        """
        if document_references is None:
            self.index = {}
            self.save_to_disk([])
            return

        if isinstance(document_references, DocumentReference):
            document_references = [document_references]

        for document_reference in document_references:
            if document_reference.doc_path in self.index:
                del self.index[document_reference.doc_path]
        self.save_to_disk([])

    def documents(
        self, document_references: Union[DocumentReference, List[DocumentReference]]
    ) -> Generator[List[Document], None, None]:
        """
        Get index document by path
        """
        if isinstance(document_references, DocumentReference):
            document_references = [document_references]

        # Find all documents with a path that is in the given list of paths
        for document_reference in document_references:
            if document_reference.doc_path in self.index:
                yield Index.Document(self.index[document_reference.doc_path])

    def document_paths(self) -> Generator[List[Document], None, None]:
        """
        Get all index documents
        """
        for document_path in list(self.index.keys()):
            yield document_path

    def index_documents(self, document_references: List[DocumentReference], **kwargs):
        """
        Create index entries
        """
        # Get documents that need to be indexed
        if kwargs.get("refresh", True) and kwargs.get("force", True):
            pass
        elif kwargs.get("refresh", True):
            document_references = self._refreshable_documents(document_references)
        else:
            document_references = self._unindexed_documents(document_references)

        ## Specify index type
        for document_reference in document_references:
            if kwargs.get("force", True):
                document_reference.doc_index_type = kwargs.get("index_type")
                continue
            document_reference.doc_index_type = (
                document_reference.doc_index_type
                if document_reference.doc_exists
                else kwargs.get("index_type")
            )

        # build search trees in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            search_tree_futures: List[Future[dict]] = [
                executor.submit(
                    create_text_search_tree,
                    read_document(
                        document_reference.doc_path, document_reference.doc_type
                    ),
                    document_reference.doc_index_type,
                )
                for document_reference in document_references
            ]

            for search_tree_future, document_reference in zip(
                search_tree_futures, document_references
            ):
                document = Index.Document.initialize(document_reference)
                document.index_type = document_reference.doc_index_type
                document.search_tree = search_tree_future.result()
                self.save_to_disk([document])
                del document_reference, search_tree_future

    def _unindexed_documents(
        self, document_references: List[DocumentReference]
    ) -> List[DocumentReference]:
        """
        Get missing documents from index
        """
        return [
            document_reference
            for document_reference in document_references
            if document_reference.doc_path not in self.index
        ]

    def _refreshable_documents(
        self, document_references: List[DocumentReference]
    ) -> List[DocumentReference]:
        """
        Get refreshable documents from index
        """
        return [
            dr
            for dr in document_references
            if self.index.get(dr.doc_path)
            and self.index.get(dr.doc_path)["hash"] != dr.doc_hash
        ]


index = Index()
