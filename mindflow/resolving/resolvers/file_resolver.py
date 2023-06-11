"""
File/Directory Resolver
"""
import os
from typing import List, Union
from mindflow.db.objects.document import DocumentReference

from mindflow.db.objects.static_definition.document import DocumentType
from mindflow.resolving.resolvers.base_resolver import BaseResolver
from mindflow.utils.files.extract import extract_files


class FileResolver(BaseResolver):
    @staticmethod
    def should_resolve(document_path: Union[str, os.PathLike]) -> bool:
        abs_path = os.path.abspath(document_path)
        return os.path.isfile(abs_path) or os.path.isdir(abs_path)

    def resolve_to_document_reference(
        self, document_path: str
    ) -> List[DocumentReference]:
        return [
            DocumentReference(path, DocumentType.FILE)
            for path in extract_files(os.path.abspath(document_path))
        ]
