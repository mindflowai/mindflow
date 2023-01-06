"""
Make a get request to the backend to check if the references are indexed.
"""
import json
import requests

from mindflow.config import Config

def request_query(query_text: str, hashes: list[str]):
    """
    This function handles the prompt generation and copying to clipboard.
    """
    response = requests.post(f"{Config.API_LOCATION}/query", json={"query_text": query_text, "reference_hashes": hashes, "auth": Config.AUTH})
    if response.status_code == 200:
        return response.json()['text']
    else:
        raise ValueError(f"Error: {response.status_code} {response.text}")
        
