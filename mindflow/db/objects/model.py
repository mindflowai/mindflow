from typing import Union

from mindflow.db.db import retrieve_object
from mindflow.db.static_definition import ObjectConfig


class Model(object):
    """Model object."""

    id: str
    name: str
    model_type: str
    hard_token_limit: int
    token_cost: int
    token_cost_unit: str

    soft_token_limit: int

    def __init__(self, params: Union[dict, None], config: ObjectConfig):
        if not params or params == {}:
            return
        self.id = params.get("id", params.get("path", None))
        self.api = params.get("api", None)
        self.name = params.get("name", None)
        self.model_type = params.get("model_type", None)
        self.hard_token_limit = params.get("hard_token_limit", None)
        self.token_cost = params.get("token_cost", None)
        self.token_cost_unit = params.get("token_cost_unit", None)

        model_config = retrieve_object(self.id, config)
        if model_config:
            self.soft_token_limit = model_config.get("soft_token_limit", None)
        if not hasattr(self, "soft_token_limit"):
            self.soft_token_limit = self.hard_token_limit // 3
