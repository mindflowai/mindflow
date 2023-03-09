import json
import os
import sys
from typing import List
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
        # Open the authentication file in read and write mode
        with open(path, "r+", encoding="utf-8") as json_file:
            # Read the existing authentication data
            return json.load(json_file)
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump({}, json_file)
    return {}


JSON_DATABASE_PATH = os.path.join(MINDFLOW_DIR, "db.json")
JSON_DATABASE = create_and_load_json(JSON_DATABASE_PATH)


class JsonDatabase(Database):
    def load(self, collection: str, object_id: str) -> Optional[dict]:
        objects = JSON_DATABASE.get(collection, None)
        if not objects:
            return None

        if isinstance(objects, dict):
            return objects.get(object_id, None)

        return None

    def load_bulk(self, collection: str, object_ids: List[str]) -> Optional[List[dict]]:
        objects = JSON_DATABASE.get(collection, None)
        if not objects:
            return None

        if isinstance(objects, dict):
            return [
                objects[object_id] for object_id in object_ids if object_id in objects
            ]

        return None

    def delete(self, collection: str, object_id: str):
        objects = JSON_DATABASE.get(collection, None)
        if not objects:
            return None

        if isinstance(objects, dict):
            if object_id in objects:
                del objects[object_id]
            else:
                print("Object not found")
                sys.exit(1)

    ### Delete objects from json from ID list and overwrite the file
    def delete_bulk(self, collection: str, object_ids: List[str]):
        if not collection in JSON_DATABASE:
            JSON_DATABASE[collection] = {}

        for object_id in object_ids:
            if JSON_DATABASE[collection].get(object_id, None):
                del JSON_DATABASE[collection][object_id]
            else:
                print("Object not found")
                sys.exit(1)

    def save(self, collection: str, value: dict):
        if not collection in JSON_DATABASE:
            JSON_DATABASE[collection] = {}

        object_id = value.get("id", None)

        if not object_id:
            print("No ID found in object")
            sys.exit(1)

        JSON_DATABASE[collection][object_id] = value

    def save_file(self):
        with open(JSON_DATABASE_PATH, "w", encoding="utf-8") as json_file:
            json.dump(JSON_DATABASE, json_file, indent=4)
