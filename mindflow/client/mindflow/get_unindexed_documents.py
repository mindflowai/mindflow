"""
Make a get request to the backend to check if the documents are indexed.
"""
import json
from typing import List, Set
import requests

from mindflow.utils.config import config as Config
from mindflow.index.model import Index


class GetUnindexedDocumentsRequest:
    """
    Unindexed document request object.
    """

    hashes: str = None
    auth: str = None

    def __init__(self, hashes: List[str], auth: str):
        self.hashes = json.dumps(hashes)
        self.auth = auth


class GetUnindexedDocumentsResponse:
    """
    Unindexed document response object.
    """

    unindexed_document_hashes: Set[str] = None

    def __init__(self, response: dict):
        self.unindexed_hashes = set(response["unindexed_document_hashes"])


def get_unindexed_documents(documents: List[Index.Document]) -> List[Index.Document]:
    """
    get request with resolved document hashes to the backend to check if they are indexed.
    """
    document_dict = {document.hash: document for document in documents}
    response = requests.post(
        f"{Config.API_LOCATION}/unindexed",
        json=vars(
            GetUnindexedDocumentsRequest(
                list(document_dict.keys()), Config.mindflow_auth()
            )
        ),
        timeout=10,
    )
    if response.status_code == 200:
        unindexed_hashes = GetUnindexedDocumentsResponse(
            response.json()
        ).unindexed_hashes
        return [document_dict[hash] for hash in unindexed_hashes]

    # Write a debug warning log here
    print(f"Error: {response.status_code} {response.text}")
    return []
