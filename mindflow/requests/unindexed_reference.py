"""
Make a get request to the backend to check if the references are indexed.
"""
import json
import requests

from mindflow.utils.config import Config


def request_unindexed_references(hashes: list[str]):
    """
    get request with resolved reference hashes to the backend to check if they are indexed.
    """
    response = requests.post(
        f"{Config.API_LOCATION}/unindexed",
        json={"hashes": json.dumps(hashes), "auth": Config.AUTH},
        timeout=10,
    )
    if response.status_code == 200:
        return response.json()["unindexed_hashes"]
    raise ValueError(f"Error: {response.status_code} {response.text}")
