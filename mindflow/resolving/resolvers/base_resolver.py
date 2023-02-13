"""
Base Resolver Class
"""

from typing import List, Optional

from mindflow.db.objects.document import DocumentReference


class BaseResolver:
    """
    Base class for resolvers
    """

    @staticmethod
    def read_document(document_path: str) -> Optional[str]:
        """
        Read a document.
        """

    @staticmethod
    def should_resolve(document_path: str) -> bool:
        """
        Checks if a string is a valid document path for this resolver.
        """
        return False

    def resolve(self, document_path: str) -> List[DocumentReference]:
        """
        Resolve a document path to text.
        """
        return []
