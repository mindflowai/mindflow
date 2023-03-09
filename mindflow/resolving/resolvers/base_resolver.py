"""
Base Resolver Class
"""
from typing import List, Dict

from mindflow.db.objects.document import DocumentReference


class BaseResolver:
    """
    Base class for resolvers
    """

    @staticmethod
    def should_resolve(document_path: str) -> bool:
        """
        Checks if a string is a valid document path for this resolver.
        """
        return False

    def resolve(self, document_path: str) -> List[Dict]:
        """
        Resolve a document path to text.
        """
        return []
