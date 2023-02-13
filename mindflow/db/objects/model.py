from typing import Optional


class Model(object):
    """Model object."""

    id: str
    api: str
    name: str
    model_type: str
    hard_token_limit: int
    token_cost: int
    token_cost_unit: str

    soft_token_limit: int

    @classmethod
    def initialize(cls, params: dict, config: Optional[dict]) -> "Model":
        new = cls()
        if not params or params == {}:
            return new
        new.id = params.get("id", params.get("path", None))
        new.api = params.get("api", None)
        new.name = params.get("name", None)
        new.model_type = params.get("model_type", None)
        new.hard_token_limit = params.get("hard_token_limit", None)
        new.token_cost = params.get("token_cost", None)
        new.token_cost_unit = params.get("token_cost_unit", None)

        if config:
            new.soft_token_limit = config.get("soft_token_limit", None)
        if not hasattr(new, "soft_token_limit"):
            new.soft_token_limit = new.hard_token_limit // 3

        return new
