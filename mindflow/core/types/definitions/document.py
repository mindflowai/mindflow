from enum import Enum


class DocumentType(Enum):
    FILE: str = "file"
    SLACK: str = "slack"
    GITHUB: str = "github"
    JIRA: str = "jira"
