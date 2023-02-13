from typing import List, Optional
from mindflow.db.objects.configurations import Configurations
from mindflow.settings import Settings
from mindflow.db.objects.document import DocumentReference

from mindflow.input import Arguments, Command
from mindflow.resolving.resolve import resolve


class State:
    """
    State of the application
    """

    user_configurations: Configurations
    settings: Settings
    arguments: Arguments
    command: str

    @property
    def document_references(self) -> List[DocumentReference]:
        document_references: List[DocumentReference] = []
        for document_path in self.arguments.document_paths:
            document_references.extend(resolve(document_path))
        return document_references

    @property
    def indexable_document_references(self) -> List[DocumentReference]:
        return [
            document_reference
            for document_reference in self.document_references
            if index_document(self.command, document_reference, self.arguments.force)
        ]


def index_document(
    command: str, document_reference: DocumentReference, force: Optional[bool]
) -> bool:
    if command == Command.REFRESH.value:
        if not document_reference.old_hash:
            return False
        if document_reference.old_hash == document_reference.hash and not force:
            return False
        return True

    if document_reference.old_hash is None:
        return True
    return False


STATE = State()
