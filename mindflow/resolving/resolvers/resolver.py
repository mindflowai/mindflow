"""Base Resolver Class"""
from typing import List
from mindflow.store.objects.document import DocumentReference
from abc import ABC, abstractmethod


class Resolver(ABC):
    @staticmethod
    @abstractmethod
    def should_resolve(document_path: str) -> bool:
        pass

    @abstractmethod
    def resolve_to_document_reference(
        self, document_path: str
    ) -> List[DocumentReference]:
        pass