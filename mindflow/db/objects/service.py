from typing import Optional
from mindflow.db.db import retrieve_object
from mindflow.db.static_definition import ObjectConfig


class Service(object):
    id: str
    name: str
    url: str
    api_url: str

    api_key: Optional[str]
    api_secret: Optional[str]

    def __init__(self, params: dict, config: ObjectConfig):
        if params is None:
            return
        self.id = params.get("id", params.get("name", None))
        self.name = params.get("name", None)
        self.url = params.get("url", None)
        self.api_url = params.get("api_url", None)

        model_config = retrieve_object(self.id, config)
        if model_config:
            self.api_key = model_config.get("api_key", None)
            self.api_secret = model_config.get("api_secret", None)
