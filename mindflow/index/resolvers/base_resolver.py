"""
Base Resolver Class
"""


from typing import List
from mindflow.index.model import DocumentReference


class BaseResolver:
    """
    Base class for resolvers
    """

    @staticmethod
    def should_resolve(document_path: str) -> bool:
        """
        Checks if a string is a valid document path for this resolver.
        """

    @staticmethod
    def resolve(document_path: str) -> List[DocumentReference]:
        """
        Resolve a document path to text.
        """
