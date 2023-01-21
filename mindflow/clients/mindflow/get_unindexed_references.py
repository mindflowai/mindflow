"""
Make a get request to the backend to check if the references are indexed.
"""
import json
from typing import List, Set
import requests

from mindflow.utils.config import config as Config


class GetUnindexedReferencesRequest:
    """
    Unindexed reference request object.
    """

    hashes: str = None
    auth: str = None

    def __init__(self, hashes: List[str], auth: str):
        self.hashes = json.dumps(hashes)
        self.auth = auth


class GetUnindexedReferencesResponse:
    """
    Unindexed reference response object.
    """

    unindexed_hashes: Set[str] = None

    def __init__(self, response: dict):
        self.unindexed_hashes = set(response["unindexed_hashes"])


def get_unindexed_references(hashes: List[str]) -> GetUnindexedReferencesResponse:
    """
    get request with resolved reference hashes to the backend to check if they are indexed.
    """
    response = requests.post(
        f"{Config.API_LOCATION}/unindexed",
        json=vars(GetUnindexedReferencesRequest(hashes, Config.mindflow_auth())),
        timeout=10,
    )
    if response.status_code == 200:
        return GetUnindexedReferencesResponse(response.json())

    # Write a debug warning log here
    print(f"Error: {response.status_code} {response.text}")
    return []
