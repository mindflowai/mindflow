"""
Configurations.
"""
import os
from mindflow.utils.auth import get_token, AuthType
from mindflow import DOT_MINDFLOW


class IndexType:
    """
    Index type enum.
    """

    DEEP: str = "deep"
    SHALLOW: str = "shallow"


class Config:
    """
    Configuration class.
    """

    API_LOCATION: str = "http://127.0.0.1:5000/api/mindflow"

    GPT_MODEL_EMBEDDING: str = "text-embedding-ada-002"
    GPT_MODEL_COMPLETION: str = "text-davinci-003"
    CHATGPT_TOKEN_LIMIT: int = 1024
    SEARCH_INDEX_TOKEN_LIMIT: int = 800
    INDEX_PATH = os.path.join(DOT_MINDFLOW, "index.json")
    INDEX_TYPE = None

    def mindflow_auth(self) -> str:
        """
        Retrieves the mindflow auth token.
        """
        return get_token(AuthType.MINDFLOW)

    def openai_auth(self) -> str:
        """
        Retrieves the openai auth token.
        """
        return get_token(AuthType.OPENAI)

    def set_deep_index(self, deep_index: bool):
        if deep_index:
            self.INDEX_TYPE = IndexType.DEEP
        else:
            self.INDEX_TYPE = IndexType.SHALLOW


# instantiates the configurations
config = Config()
