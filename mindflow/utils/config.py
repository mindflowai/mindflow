"""
Configurations
"""
import os
from mindflow.utils.auth import get_token, AuthType

# Create and instantiate a configuration class that gives you the API location and the Auth
class Config:
    """
    Configuration class
    """

    API_LOCATION: str = "http://127.0.0.1:5000/api/mindflow"

    GPT_MODEL_EMBEDDING: str = "text-embedding-ada-002"
    GPT_MODEL_COMPLETION: str = "text-davinci-003"
    CHATGPT_TOKEN_LIMIT: int = 1024

    def mindflow_auth(self) -> str:
        return get_token(AuthType.Mindflow)

    def openai_auth(self) -> str:
        return get_token(AuthType.OpenAI)


# instantiates the configurations
config = Config()
