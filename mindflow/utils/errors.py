GITHUB_ISSUE_MESSAGE = "If the problem persists, please raise an issue at: https://github.com/nollied/mindflow-cli/issues"
CONNECTION_MESSAGE = "Please check your internet connection and try again."


class ModelError(Exception):
    """Base class for all exceptions raised by this module."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    @property
    def base_message(self):
        return f"Model API failed to return response for chat/query. {CONNECTION_MESSAGE}. {GITHUB_ISSUE_MESSAGE}."

    @property
    def commit_message(self):
        return f"Model API failed to return response for commit. {CONNECTION_MESSAGE}. {GITHUB_ISSUE_MESSAGE}"

    @property
    def diff_message(self):
        return f"Model API failed to return response for diff. {CONNECTION_MESSAGE}. {GITHUB_ISSUE_MESSAGE}"

    @property
    def diff_partial_message(self):
        return f"Warning: model API failed to return response for part of, or entire, diff. {CONNECTION_MESSAGE}. {GITHUB_ISSUE_MESSAGE}"

    @property
    def pr_message(self):
        return f"Model API failed to return response for pr/mr. {CONNECTION_MESSAGE}. {GITHUB_ISSUE_MESSAGE}"

    @property
    def index_message(self):
        return f"Warning: Model API failed to return response for a document chunk. {CONNECTION_MESSAGE}. {GITHUB_ISSUE_MESSAGE}"

    @property
    def query_message(self):
        return f"Model API failed to return response for query. {CONNECTION_MESSAGE}. {GITHUB_ISSUE_MESSAGE}"

    @property
    def embedding_message(self):
        return f"Warning: Model API failed to return response for embedding. {CONNECTION_MESSAGE}. {GITHUB_ISSUE_MESSAGE}"


class EmbeddingModelError(Exception):
    """Base class for all exceptions raised by this module."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
