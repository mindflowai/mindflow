from copy import deepcopy
import json

from typing import List, Optional
from mindflow.db.static_definition import ObjectConfig, db


def retrieve_object_json(object_id: str, object_config: ObjectConfig) -> Optional[dict]:
    file = deepcopy(db)

    objects = file.get(object_config.collection, None)
    if not objects:
        return None

    if isinstance(objects, dict):
        return objects.get(object_id, None)

    return None


def retrieve_object_json_bulk(
    object_ids: List[str], object_config: ObjectConfig
) -> Optional[List[dict]]:
    file = deepcopy(db)

    # print(file)
    objects = file.get(object_config.collection, None)
    if not objects:
        return None

    if isinstance(objects, dict):
        return [objects[object_id] for object_id in object_ids if object_id in objects]

    return None


### Delete objects from json from ID list and overwrite the file
def delete_object_json_bulk(object_ids: List[str], object_config: ObjectConfig):

    collection = db.get(object_config.collection, None)
    if not collection:
        db[object_config.collection] = {}

    for object_id in object_ids:
        if db[object_config.collection].get(object_id, None):
            del db[object_config.collection][object_id]

    print(object_config.path)
    with open(object_config.path, "w", encoding="utf-8") as file:
        json.dump(db, file, indent=4)


def set_object_json(object_id: str, value: dict, object_config: ObjectConfig):
    collection = db.get(object_config.collection, None)
    if not collection:
        db[object_config.collection] = {}

    db[object_config.collection][object_id] = value
    with open(object_config.path, "w", encoding="utf-8") as file:
        json.dump(db, file, indent=4)
