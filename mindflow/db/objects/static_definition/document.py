from mindflow.utils.enum import ExtendedEnum


class DocumentArgument(ExtendedEnum):
    """
    Document argument enum
    """

    DOCUMENT_TYPE: str = "document_type"
    PATH: str = "path"
    HASH: str = "hash"
    INDEX_TYPE: str = "index_type"
    SEARCH_TREE: str = "search_tree"
    SIZE: str = "size"


class DocumentType(ExtendedEnum):
    """
    Document type enum
    """

    FILE: str = "file"
    SLACK: str = "slack"
    GITHUB: str = "github"
    JIRA: str = "jira"
