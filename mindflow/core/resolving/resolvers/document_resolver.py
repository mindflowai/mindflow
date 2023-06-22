from typing import List
from mindflow.core.types.document import DocumentReference
from abc import ABC, abstractmethod


class DocumentResolver(ABC):
    @staticmethod
    @abstractmethod
    def should_resolve(document_path: str) -> bool:
        pass

    @abstractmethod
    def resolve_to_document_reference(
        self, document_path: str
    ) -> List[DocumentReference]:
        pass
