"""
Resolves a URL to a text file.
"""
from urllib.parse import unquote
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from mindflow.resolve.resolvers.base_resolver import BaseResolver


class URLResolver(BaseResolver):
    """
    Resolver for URLs to text.
    """

    def __init__(self, reference):
        self.reference = reference

    def _get_clean_html(self) -> str:
        res = requests.get(self.reference)
        # Parse the HTML content of the website
        soup = BeautifulSoup(res.content, "html.parser")
        # Extract and clean the text from the website
        return soup.get_text().strip().replace("\n", " ").replace("\r", "")

    def should_resolve(self) -> bool:
        """
        Checks if a string is a valid URL.
        """
        try:
            result = urlparse(self.reference)
            return all([result.scheme, unquote(result.netloc)])
        except ValueError:
            return False

    def resolve(self) -> dict:
        """
        Resolve a URL to text.
        """
        return {"text": self._get_clean_html(), "type": "url"}
