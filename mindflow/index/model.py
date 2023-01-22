"""
Index model
"""

from asyncio import Future
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
import os
from typing import List, Dict

import numpy as np

from mindflow.utils.reference import Reference
from mindflow.client.openai.gpt import GPT
from mindflow.utils.config import config as Config
from mindflow import DOT_MINDFLOW

INDEX_PATH = os.path.join(DOT_MINDFLOW, "index.json")

class Index:
    """
    Index model
    """

    class Document:
        """
        Index model
        """

        path: str = None
        type: str = None
        hash: str = None
        summary: str = None
        embedding: List[float] = None
        size: int = None

        def __init__(self, index_data):
            if index_data is not None:
                self.path: str = index_data.get("path")
                self.type: str = index_data.get("type")
                self.hash: str = index_data.get("hash")
                self.embedding: List[float] = index_data.get("embedding")
                self.size: int = index_data.get("size")
                self.last_updated: datetime = index_data.get("last_updated")
                self.created_at: datetime = index_data.get("created_at")

        def read(self) -> str:
            """
            Read file
            """
            with open(self.path, "r") as file:
                return file.read()

        def get_summary(self) -> str:
            """
            Get index
            """
            return self.summary

        def get_embedding(self) -> List[float]:
            """
            Get embedding as numpy array
            """
            return np.array(self.embedding)


    index: Dict[str, Document]

    def __init__(self):
        self.index_json = self.load()

    def load(self) -> dict:
        if os.path.isfile(INDEX_PATH):

            # Open the authentication file in read and write mode
            with open(INDEX_PATH, "r+") as index_file:
                # Read the existing authentication data
                return json.load(index_file)
        else:
            return {}

    def save(self, documents: List[Document]):
        """
        Add index entries to database
        """
        update = {document.hash: vars(document) for document in documents}
        self.index_json.update(update)
        with open(INDEX_PATH, "w") as auth_file:
            json.dump(self.index_json, auth_file)

    def get_missing_hashes(self, hashes: List[str]) -> List[str]:
        """
        Get missing indices by hashes
        """
        return [key for key in hashes if key not in self.index_json]

    def create_entries(self, references: List[Reference]):
        """
        Create index entries
        """
        entries: List["Index"] = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Start a separate thread for each reference
            future_to_reference: dict[Future[Index], Reference] = {
                executor.submit(self._create_index, reference): reference
                for reference in references
            }

            # Wait for all threads to complete
            for future in as_completed(future_to_reference):
                try:
                    index: "Index" = future.result()
                except Exception as error:
                    print(f"Error creating document for reference {error}")
                else:
                    entries.append(index)
        if len(entries) != 0:
            self.save(entries)

    def get_document_by_hash(self, hashes: List[str]) -> List["Index"]:
        """
        Get index document by hash
        """
        # Find all documents with a hash that is in the given list of hashes
        entries: dict = [
            self.index_json[hash] for hash in hashes if hash in self.index_json
        ]
        # Return a list of cls objects constructed from the found documents
        return [Index.Document(index) for index in entries]

    @staticmethod
    def _create_index(reference: Reference) -> Document:
        """
        Create index document
        """
        return Index.Document(
            {
                "path": reference.path,
                "type": reference.type,
                "hash": reference.hash,
                "text": reference.text,
                "embedding": GPT.get_embedding(
                    reference.text, Config.GPT_MODEL_EMBEDDING
                ),
                "size": reference.size,
            }
        )


index = Index()
