from enum import Enum


class DocumentType(Enum):
    """
    Document type enum
    """

    FILE: str = "file"
    SLACK: str = "slack"
    GITHUB: str = "github"
    JIRA: str = "jira"
