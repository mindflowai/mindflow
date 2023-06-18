from mindflow.utils.enum import ExtendedEnum


class DocumentType(ExtendedEnum):
    """
    Document type enum
    """

    FILE: str = "file"
    SLACK: str = "slack"
    GITHUB: str = "github"
    JIRA: str = "jira"
