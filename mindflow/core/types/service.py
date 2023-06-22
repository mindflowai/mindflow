from mindflow.core.types.store_traits.json import JsonStore
from mindflow.core.types.store_traits.static import StaticStore
from mindflow.core.types.definitions.service import ServiceID


class Service(StaticStore):
    id: str
    name: str
    url: str
    api_url: str


class ServiceConfig(JsonStore):
    id: str
    api_key: str
    api_secret: str
    environment: str


class ConfiguredService:
    id: str
    name: str
    url: str
    api_url: str

    api_key: str
    api_secret: str
    environment: str

    def __init__(self, service_id: str):
        if service := Service.load(service_id):
            for key, value in service.__dict__.items():
                setattr(self, key, value)

        if service_config := ServiceConfig.load(f"{service_id}_config"):
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

    @property
    def anthropic(self) -> ConfiguredService:
        if ServiceID.ANTHROPIC.value not in self._services:
            self._services[ServiceID.ANTHROPIC.value] = ConfiguredService(
                ServiceID.ANTHROPIC.value
            )
        return self._services[ServiceID.ANTHROPIC.value]

    @property
    def pinecone(self) -> ConfiguredService:
        if ServiceID.PINECONE.value not in self._services:
            self._services[ServiceID.PINECONE.value] = ConfiguredService(
                ServiceID.PINECONE.value
            )
        return self._services[ServiceID.PINECONE.value]
