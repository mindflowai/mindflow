import os
from typing import List, Union
from mindflow.core.types.document import DocumentReference

from mindflow.core.types.definitions.document import DocumentType
from mindflow.core.resolving.resolvers.document_resolver import DocumentResolver
from mindflow.core.file_processing.extract import extract_files_from_directory


class FileResolver(DocumentResolver):
    @staticmethod
    def should_resolve(document_path: Union[str, os.PathLike]) -> bool:
        return os.path.isfile(
            (abs_path := os.path.abspath(document_path))
        ) or os.path.isdir(abs_path)

    def resolve_to_document_reference(
        self, document_path: str
    ) -> List[DocumentReference]:
        return [
            DocumentReference(path, DocumentType.FILE)
            for path in extract_files_from_directory(os.path.abspath(document_path))
        ]
