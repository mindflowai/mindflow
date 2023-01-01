import json
import requests
from mindflow.config import API_LOCATION
from mindflow.resolve.resolvers.path_resolver import PathResolver
from mindflow.utils.reference import Reference
from mindflow.config import config


class QueryRequestHandler():
    """
    This class is used to generate a query prompt request.
    """
    def __init__(self, query_text: str, references: list):
        self.query_text = query_text
        self.references = references

    @staticmethod
    def _resolve(references: list) -> dict[str, Reference]:
        """
        Resolves a reference to text.
        """
        resolved_references = {}
        for reference in references:
            resolved = False
            resolvers = [PathResolver(reference)]

            for resolver in resolvers:
                if resolver.should_resolve():
                    resolved = True
                    resolved_references.update(resolver.resolve())

            if not resolved:
                raise ValueError(f"Cannot resolve reference: {reference}")
        
        return resolved_references

    def _request_unindexed_references(self, hashes: list[str]):
        """
        This function makes a get request with resolved reference hashes to the backend to check if they are indexed.
        """
        response = requests.post(f"{API_LOCATION}/unindexed", json={"hashes": json.dumps(hashes), "auth": config.AUTH})
        if response.status_code == 200:
            return response.json()['unindexed_hashes']
        else:
            raise ValueError(f"Error: {response.status_code} {response.text}")
    
    def _request_index_references(self, resolved_references: dict[str, Reference],  unindexed_hashes: list):
        """
        This function makes a post request to the backend to index the unindexed references.
        """
        if len(unindexed_hashes) == 0:
            return
        unindexed_references = [resolved_references[unindexed_reference].__dict__ for unindexed_reference in unindexed_hashes]
        response = requests.post(f"{API_LOCATION}/index", json={"references": json.dumps(unindexed_references), "auth": config.AUTH})
        if response.status_code != 200:
            raise ValueError(f"Error: {response.status_code} {response.text}")
    
    def query(self):
        """
        This function handles the prompt generation and copying to clipboard.
        """
        resolved_references = self._resolve(self.references)
        unindexed_hashes = self._request_unindexed_references(list(resolved_references.keys()))
        self._request_index_references(resolved_references, unindexed_hashes)
        response = requests.post(f"{API_LOCATION}/query", json={"query_text": self.query_text, "reference_hashes": list(resolved_references.keys()), "auth": config.AUTH})
        if response.status_code == 200:
            return response.json()['text']
        else:
            raise ValueError(f"Error: {response.status_code} {response.text}")
            
