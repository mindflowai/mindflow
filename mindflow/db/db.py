# Generic accessors

import sys
from typing import List, Optional

from mindflow.db.locations.json import (
    delete_object_json_bulk,
    retrieve_object_json,
    retrieve_object_json_bulk,
    set_object_json,
)
from mindflow.db.locations.static import retrieve_object_static
from mindflow.db.static_definition import ObjectConfig, ObjectStoreType


class Database:
    def __init__(self, object_config: ObjectConfig):
        self.object_config = object_config

    def retrieve_object(self, object_id: str) -> Optional[dict]:
        return retrieve_object(object_id, self.object_config)

    def retrieve_object_bulk(self, object_ids: List[str]) -> Optional[List[dict]]:
        return retrieve_object_bulk(object_ids, self.object_config)

    def set_object(self, object_id: str, value: dict):
        set_object(object_id, value, self.object_config)

    def delete_object_bulk(self, object_ids: List[str]):
        delete_object_bulk(object_ids, self.object_config)


### Retrieval Operations ###
def retrieve_object(object_id: str, object_config: ObjectConfig) -> Optional[dict]:
    object: Optional[dict]
    match object_config.store:
        case ObjectStoreType.STATIC.value:
            object = retrieve_object_static(object_id, object_config).value
        case ObjectStoreType.JSON.value:
            object = retrieve_object_json(object_id, object_config)
        case _:
            print(
                f"Invalid object location {object_config.store}. Please check your configuration file or raise an issue."
            )
            sys.exit(1)
    return object


### Set Operations ###
def set_object(object_id: str, value: dict, object_config: ObjectConfig):
    match object_config.store:
        case ObjectStoreType.JSON.value:
            set_object_json(object_id, value, object_config)
        case _:
            print(
                f"Invalid object location {object_config.store}. Please check your configuration file or raise an issue."
            )
            sys.exit(1)


### Retrieval Operations ###
def retrieve_object_bulk(
    object_ids: List[str], object_config: ObjectConfig
) -> Optional[List[dict]]:
    objects: Optional[List[dict]]
    match object_config.store:
        case ObjectStoreType.JSON.value:
            objects = retrieve_object_json_bulk(object_ids, object_config)
        case _:
            print(
                f"Invalid object location {object_config.store}. Please check your configuration file or raise an issue."
            )
            sys.exit(1)
    return objects


### Delete Operations ###
def delete_object_bulk(object_ids: List[str], object_config: ObjectConfig):
    match object_config.store:
        case ObjectStoreType.JSON.value:
            delete_object_json_bulk(object_ids, object_config)
        case _:
            print(
                f"Invalid object location {object_config.store}. Please check your configuration file or raise an issue."
            )
            sys.exit(1)


def filter_object(object_key: str, filter: str, object_config: ObjectConfig):
    match object_config.store:
        case ObjectStoreType.JSON.value:
            object = retrieve_object_json(object_key, object_config.path)
            if not object:
                print(f"Invalid object key {object_key}. Please raise an issue.")
                sys.exit(1)
            filtered_object = {}
            for key, value in object.items():
                if filter in key:
                    filtered_object[key] = value
            set_object_json(object_key, filtered_object, object_config.path)
        case _:
            print(
                f"Invalid object store {object_config.store}. Please check your configuration file or raise an issue."
            )
            sys.exit(1)
