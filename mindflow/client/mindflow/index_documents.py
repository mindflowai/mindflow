"""
Request to index documents.
"""

import json
from typing import List
import requests

from mindflow.utils.config import config as CONFIG
from mindflow.index.model import Index


class IndexDocumentsRequest:
    """
    Index request object.
    """

    documents: str = None
    auth: str = None

    def __init__(self, unindexed_documents: List[Index.Document], auth: str):
        self.documents = json.dumps(
            [vars(unindexed_document) for unindexed_document in unindexed_documents]
        )
        self.auth = auth


def index_documents(unindexed_documents: List[Index.Document]) -> None:
    """
    This function makes a post request to the backend to index the unindexed documents.
    """
    response = requests.post(
        f"{CONFIG.API_LOCATION}/index",
        json=vars(IndexDocumentsRequest(unindexed_documents, CONFIG.mindflow_auth())),
        timeout=10,
    )
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")
