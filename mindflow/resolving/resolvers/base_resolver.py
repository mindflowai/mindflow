"""Base Resolver Class"""
from typing import List
from mindflow.db.objects.document import DocumentReference
from abc import ABC, abstractmethod


class BaseResolver(ABC):
    @staticmethod
    @abstractmethod
    def should_resolve(document_path: str) -> bool:
        """Checks if a string is a valid document path for this resolver."""
        pass

    def resolve_to_document_reference(
        self, document_path: str
    ) -> List[DocumentReference]:
        pass
