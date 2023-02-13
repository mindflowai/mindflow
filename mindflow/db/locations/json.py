import json
import os
import sys

from typing import List, Optional

MINDFLOW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mindflow")


class JsonDatabase:
    def __init__(self):
        if not os.path.exists(MINDFLOW_DIR):
            os.makedirs(MINDFLOW_DIR)

        def create_and_load_json(path: str) -> dict:
            if os.path.exists(path):
                print(path)
                # Open the authentication file in read and write mode
                with open(path, "r+", encoding="utf-8") as json_file:
                    # Read the existing authentication data
                    return json.load(json_file)
            with open(path, "w", encoding="utf-8") as json_file:
                json.dump({}, json_file)
            return {}

        self.file = create_and_load_json(self.path)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as json_file:
            json.dump(self.file, json_file, indent=4)

    @property
    def path(self):
        return os.path.join(MINDFLOW_DIR, "db.json")

    def retrieve_object(self, collection: str, object_id: str) -> Optional[dict]:
        objects = self.file.get(collection, None)
        if not objects:
            return None

        if isinstance(objects, dict):
            return objects.get(object_id, None)

        return None

    def retrieve_object_bulk(
        self, collection: str, object_ids: List[str]
    ) -> Optional[List[dict]]:
        objects = self.file.get(collection, None)
        if not objects:
            return None

        if isinstance(objects, dict):
            return [
                objects[object_id] for object_id in object_ids if object_id in objects
            ]

        return None

    ### Delete objects from json from ID list and overwrite the file
    def delete_object_bulk(self, collection: str, object_ids: List[str]):
        if not collection in self.file:
            self.file[collection] = {}

        for object_id in object_ids:
            if self.file[collection].get(object_id, None):
                del self.file[collection][object_id]

    def set_object(self, collection: str, value: dict):
        if not collection in self.file:
            self.file[collection] = {}

        object_id = value.get("id", None)
        if not object_id:
            print("No ID found in object")
            sys.exit(1)

        self.file[collection][object_id] = value
