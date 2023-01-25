"""
Make a get request to the backend to check if the documents are indexed.
"""
from typing import List
import requests

from mindflow.utils.config import config as CONFIG


class QueryRequest:
    """
    Query request object.
    """

    query_text: str = None
    document_hashes: List[str] = None
    return_prompt: bool = None
    auth: str = None

    def __init__(
        self,
        query_text: str,
        document_hashes: List[str],
        return_prompt: bool,
        auth: str,
    ):
        self.query_text = query_text
        self.document_hashes = document_hashes
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
        f"{CONFIG.API_LOCATION}/query",
        json=vars(
            QueryRequest(query_text, hashes, return_prompt, CONFIG.mindflow_auth())
        ),
        timeout=10,
    )
    if response.status_code == 200:
        return QueryResponse(response.json())
    raise ValueError(f"Error: {response.status_code} {response.text}")
