import json
import os

from typing import Dict, List
from typing import Optional

from mindflow.db.db.database import Database


def get_mindflow_dir():
    if os.name == "nt":  # Check if the OS is Windows
        config_dir = os.getenv("APPDATA")
    else:
        config_dir = os.path.join(os.path.expanduser("~"), ".config")
    mindflow_dir = os.path.join(config_dir, "mindflow")
    return mindflow_dir


MINDFLOW_DIR = get_mindflow_dir()
if not os.path.exists(MINDFLOW_DIR):
    os.makedirs(MINDFLOW_DIR)


def create_and_load_json(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r+", encoding="utf-8") as json_file:
            return json.load(json_file)
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump({}, json_file)
    return {}


JSON_DATABASE_PATH = os.path.join(MINDFLOW_DIR, "db.json")


class JsonDatabase(Database):
    def __init__(self):
        self.collections: dict = create_and_load_json(JSON_DATABASE_PATH)

    def load(self, collection: str, object_id: str) -> Optional[dict]:
        objects = self.collections.get(collection, None)
        if not objects:
            return None

        return objects.get(object_id, None)

    def load_bulk(self, collection: str, object_ids: List[str]) -> List[Optional[dict]]:
        objects = self.collections.get(collection, None)
        if not objects:
            return []

        return [objects.get(object_id, None) for object_id in object_ids]

    def delete(self, collection: str, object_id: str):
        objects = self.collections.get(collection, None)
        if not objects:
            return None

        objects.pop(object_id, None)

    def delete_bulk(self, collection: str, object_ids: List[str]):
        objects = self.collections.get(collection, None)
        if not objects:
            return None

        for object_id in object_ids:
            objects.pop(object_id, None)

    def save(self, collection: str, value: dict):
        objects = self.collections.get(collection, None)
        if not objects:
            return None

        object_id = value.get("id", None)
        if not object_id:
            raise ValueError("No ID found in object")

        objects[object_id] = value

    def save_bulk(self, collection: str, values: List[dict]):
        objects = self.collections.get(collection, None)
        if not objects:
            return None

        for value in values:
            object_id = value.get("id", None)
            if not object_id:
                raise ValueError("No ID found in object")

            objects[object_id] = value

    def save_file(self):
        with open(JSON_DATABASE_PATH, "w", encoding="utf-8") as json_file:
            json.dump(self.collections, json_file, indent=4)

    def __del__(self):
        self.save_file()
