"""
Configurations.
"""
from mindflow.utils.auth import get_token, AuthType


class Config:
    """
    Configuration class.
    """

    API_LOCATION: str = "http://127.0.0.1:5000/api/mindflow"

    GPT_MODEL_EMBEDDING: str = "text-embedding-ada-002"
    GPT_MODEL_COMPLETION: str = "text-davinci-003"
    CHATGPT_TOKEN_LIMIT: int = 1024
    SEARCH_INDEX_TOKEN_LIMIT: int = 1500

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


# instantiates the configurations
config = Config()
