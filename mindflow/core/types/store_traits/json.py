import json
import os

from typing import List, Type, TypeVar, Union
from typing import Optional


def get_mindflow_dir():
    config_dir = (
        os.getenv("APPDATA")
        if os.name == "nt"
        else os.path.join(os.path.expanduser("~"), ".config")
    )
    return os.path.join(config_dir, "mindflow")


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
collections: dict = create_and_load_json(JSON_DATABASE_PATH)


def save_json_store():
    with open(JSON_DATABASE_PATH, "w", encoding="utf-8") as json_file:
        json.dump(collections, json_file, indent=4)


T = TypeVar("T", bound="JsonStore")


class JsonStore:
    id: str

    def __init__(self, id: Union[str, dict]):
        if isinstance(id, dict):
            if not "id" in id:
                raise ValueError("id is required")
            for key, value in id.items():
                setattr(self, key, value)
        else:
            self.id = id

    @classmethod
    def load(cls: Type[T], object_id: str) -> Optional[T]:
        objects = collections.get(cls.__name__, {})
        object = objects.get(object_id)
        return cls(object) if object else None

    @classmethod
    def load_bulk(cls: Type[T], object_ids: List[str]) -> List[Optional[T]]:
        objects = collections.get(cls.__name__, {})
        loaded_objects: List[Optional[T]] = [
            cls(objects[object_id]) if objects.get(object_id) else None
            for object_id in object_ids
        ]
        return loaded_objects

    @classmethod
    def load_bulk_ignore_missing(cls: Type[T], object_ids: List[str]) -> List[T]:
        objects = collections.get(cls.__name__, {})
        loaded_objects: List[Optional[T]] = [
            cls(objects[object_id]) if (objects.get(object_id)) else None
            for object_id in object_ids
        ]
        return list(filter(None, loaded_objects))

    @classmethod
    def delete(cls, object_id: str):
        if not (objects := collections.get(cls.__name__, None)):
            return None

        objects.pop(object_id, None)

    @classmethod
    def delete_bulk(cls, object_ids: List[str]):
        if not (objects := collections.get(cls.__name__, None)):
            return None

        for object_id in object_ids:
            objects.pop(object_id, None)

    def save(self):
        if not (objects := collections.get(self.__class__.__name__, {})):
            collections[self.__class__.__name__] = objects

        if not hasattr(self, "id"):
            raise ValueError("No ID found in object")

        objects[self.id] = self.__dict__

    @classmethod
    def save_bulk(cls, objects: List[T]):
        if not (saved_objects := collections.get(cls.__name__, {})):
            collections[cls.__name__] = saved_objects

        for object in objects:
            if not hasattr(object, "id"):
                raise ValueError("No ID found in object")

            saved_objects[object.id] = object.__dict__
