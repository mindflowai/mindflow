"""
Configurations
"""
import os
from mindflow.utils.token import get_token, AuthType

# Create and instantiate a configuration class that gives you the API location and the Auth
class Config:
    """
    Configuration class
    """

    API_LOCATION: str = "http://127.0.0.1:5000/api/mindflow"

    def mindflow_auth(self) -> str:
        return get_token(AuthType.Mindflow)


# instantiates the configurations
config = Config()
