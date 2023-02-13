from typing import Optional


class Service(object):
    id: str
    name: str
    url: str
    api_url: str

    api_key: Optional[str]
    api_secret: Optional[str]

    @classmethod
    def initialize(cls, params: dict, config: Optional[dict]) -> "Service":
        new = cls()
        if not params or params == {}:
            return new
        new.id = params.get("id", params.get("name", None))
        new.name = params.get("name", None)
        new.url = params.get("url", None)
        new.api_url = params.get("api_url", None)

        if config:
            new.api_key = config.get("api_key", None)
            new.api_secret = config.get("api_secret", None)
        return new
