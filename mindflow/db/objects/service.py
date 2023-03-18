from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.db.database import Collection
from mindflow.db.objects.base import BaseObject
from mindflow.db.objects.static_definition.service import ServiceID


class Service(BaseObject):
    id: str
    name: str
    url: str
    api_url: str

    _collection: Collection = Collection.SERVICE
    _database = DATABASE_CONTROLLER.databases.json


class ServiceConfig(BaseObject):
    """Service config object."""

    id: str
    api_key: str
    api_secret: str

    _collection: Collection = Collection.CONFIGURATIONS
    _database = DATABASE_CONTROLLER.databases.json


class ConfiguredService:
    id: str
    name: str
    url: str
    api_url: str

    api_key: str
    api_secret: str

    def __init__(self, service_id: str):
        service = Service.load(service_id)
        service_config = ServiceConfig.load(f"{service_id}_config")

        if service:
            for key, value in service.__dict__.items():
                setattr(self, key, value)

        if service_config:
            for key, value in service_config.__dict__.items():
                if value not in [None, ""]:
                    setattr(self, key, value)


class ConfiguredServices:
    def __init__(self):
        self._services = {}

    @property
    def openai(self) -> ConfiguredService:
        if ServiceID.OPENAI.value not in self._services:
            self._services[ServiceID.OPENAI.value] = ConfiguredService(
                ServiceID.OPENAI.value
            )
        return self._services[ServiceID.OPENAI.value]
