"""
Make a get request to the backend to check if the references are indexed.
"""
import json
from typing import List
import requests

from mindflow.utils.config import Config


class UnindexedReferenceRequest:
    """
    Unindexed reference request object.
    """

    hashes: str = None
    auth: str = None

    def __init__(self, hashes: List[str], auth: str):
        self.hashes = json.dumps(hashes)
        self.auth = auth


class UnindexedReferenceResponse:
    """
    Unindexed reference response object.
    """

    unindexed_hashes: List[str] = None

    def __init__(self, response: dict):
        self.unindexed_hashes = response["unindexed_hashes"]


def request_unindexed_references(hashes: List[str]) -> UnindexedReferenceResponse:
    """
    get request with resolved reference hashes to the backend to check if they are indexed.
    """
    response = requests.post(
        f"{Config.API_LOCATION}/unindexed",
        json=vars(UnindexedReferenceRequest(hashes, Config.AUTH)),
        timeout=10,
    )
    if response.status_code == 200:
        return UnindexedReferenceResponse(response.json())

    # Write a debug warning log here
    print(f"Error: {response.status_code} {response.text}")
    return []
