"""
Base Resolver Class
"""

from typing import List, Optional

from mindflow.db.objects.document import DocumentReference
from mindflow.db.static_definition import ObjectConfig


class BaseResolver:
    """
    Base class for resolvers
    """

    @staticmethod
    def read_document(self, document_path: str) -> Optional[str]:
        """
        Read a document.
        """

    @staticmethod
    def should_resolve(document_path: str) -> bool:
        """
        Checks if a string is a valid document path for this resolver.
        """

    def resolve(self, document_path: str, document_config: ObjectConfig) -> List[DocumentReference]:
        """
        Resolve a document path to text.
        """
