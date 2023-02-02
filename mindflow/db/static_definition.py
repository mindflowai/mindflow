import json
import os
from mindflow.utils.enum import ExtendedEnum


class ObjectStoreType(ExtendedEnum):
    STATIC = "static"
    JSON = "json"


class Collection(ExtendedEnum):
    SERVICE = "service"
    SERVICE_CONFIG = "service_config"
    MODEL = "model"
    MODEL_CONFIG = "model_config"
    MINDFLOW_MODEL_CONFIG = "mindflow_model_config"
    DOCUMENT = "document"


class ObjectName(ExtendedEnum):
    SERVICE = "Service"
    SERVICE_CONFIG = "Service Configurations"
    MODEL = "Model"
    MODEL_CONFIG = "Model Configurations"
    MINDFLOW_MODEL_CONFIG = "Mindflow Model Configurations"
    DOCUMENT = "Document"


MINDFLOW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".mindflow")
JSON_DB_PATH = os.path.join(MINDFLOW_DIR, "db.json")
if not os.path.exists(MINDFLOW_DIR):
    os.makedirs(MINDFLOW_DIR)


def create_and_load_json(path: str) -> dict:
    if os.path.isfile(path):
        # Open the authentication file in read and write mode
        with open(path, "r+", encoding="utf-8") as json_file:
            # Read the existing authentication data
            return json.load(json_file)
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump({}, json_file)
    return {}


db = create_and_load_json(JSON_DB_PATH)


class ObjectConfig:
    def __init__(self, store: str, collection: str, path: str):
        self.store = store
        self.collection = collection
        self.path = path
