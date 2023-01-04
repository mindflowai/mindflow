import os

from mindflow.utils.token import get_token

# Create and instantiate a configuration class that gives you the API location and the Auth
class Config(object):
    API_LOCATION = "http://127.0.0.1:5000/api/mindflow"
    AUTH = get_token()

# instantia the configurations 
config = Config()