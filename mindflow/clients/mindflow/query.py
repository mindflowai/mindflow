"""
Make a get request to the backend to check if the references are indexed.
"""
from typing import List
import requests

from mindflow.utils.config import config as Config


class QueryRequest:
    """
    Query request object.
    """

    query_text: str = None
    reference_hashes: List[str] = None
    return_prompt: bool = None
    auth: str = None

    def __init__(
        self,
        query_text: str,
        reference_hashes: List[str],
        return_prompt: bool,
        auth: str,
    ):
        self.query_text = query_text
        self.reference_hashes = reference_hashes
        self.return_prompt = return_prompt
        self.auth = auth


class QueryResponse:
    """
    Query response object.
    """

    text: str = None

    def __init__(self, response: dict):
        self.text = response["text"]


def query(
    query_text: str, hashes: List[str], return_prompt: bool = False
) -> QueryResponse:
    """
    This function handles the prompt generation and copying to clipboard.
    """
    response = requests.post(
        f"{Config.API_LOCATION}/query",
        json=vars(
            QueryRequest(query_text, hashes, return_prompt, Config.mindflow_auth())
        ),
        timeout=10,
    )
    if response.status_code == 200:
        return QueryResponse(response.json())
    raise ValueError(f"Error: {response.status_code} {response.text}")
