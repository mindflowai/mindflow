"""
Base Resolver Class
"""
from typing import List
from mindflow.db.objects.document import DocumentReference


class BaseResolver:
    @staticmethod
    def should_resolve(document_path: str) -> bool:
        """
        Checks if a string is a valid document path for this resolver.
        """
        return False

    def resolve_to_document_reference(
        self, document_path: str
    ) -> List[DocumentReference]:
        document_references: List[DocumentReference] = []
        return document_references
