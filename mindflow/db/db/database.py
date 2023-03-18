from typing import List
from typing import Optional

from mindflow.utils.enum import ExtendedEnum


class Store(ExtendedEnum):
    STATIC = "static"
    JSON = "json"
    NEO4J = "neo4j"


class Collection(ExtendedEnum):
    SERVICE = "service"
    MODEL = "model"
    MIND_FLOW_MODEL = "mind_flow_model"
    CONFIGURATIONS = "configurations"
    DOCUMENT = "document"


class Database:
    def load(self, collection: str, object_id: str) -> Optional[dict]:
        raise NotImplementedError

    def load_bulk(self, collection: str, object_ids: List[str]) -> List[Optional[dict]]:
        raise NotImplementedError

    def delete(self, collection: str, object_id: str):
        raise NotImplementedError

    def delete_bulk(self, collection: str, object_ids: List[str]):
        raise NotImplementedError

    def save(self, collection: str, value: dict):
        raise NotImplementedError

    def save_bulk(self, collection: str, values: List[dict]):
        raise NotImplementedError
