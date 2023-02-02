from typing import Type, Union
from mindflow.db.objects.static_definition.model import (
    ModelTextEmbeddingOpenAI,
    ModelTextCompletionOpenAI,
    ModelOpenAI,
)

from mindflow.utils.enum import ExtendedEnum


class ServiceID(ExtendedEnum):
    OPENAI = "openai"


class ServiceParameterKey(ExtendedEnum):
    ID = "id"
    NAME = "name"
    URL = "url"
    API_URL = "api_url"


class ServiceConfigParameterKey(ExtendedEnum):
    API_KEY = "api_key"
    API_SECRET = "api_secret"


class ServiceConfigParameterName(ExtendedEnum):
    API_KEY = "API Key"
    API_SECRET = "API Secret"


class ServiceName(ExtendedEnum):
    OPENAI = "OpenAI"


class ServiceURL(ExtendedEnum):
    OPENAI = ""


## Service Model Types
class ServiceModelTypeTextEmbedding(ExtendedEnum):
    OPENAI = ModelTextEmbeddingOpenAI


class ServiceModelTypeTextCompletion(ExtendedEnum):
    OPENAI = ModelTextCompletionOpenAI


class ServiceModel(ExtendedEnum):
    OPENAI = ModelOpenAI


class ServiceStatic(ExtendedEnum):
    OPENAI: dict = {
        ServiceParameterKey.ID.value: ServiceID.OPENAI.value,
        ServiceParameterKey.NAME.value: ServiceName.OPENAI.value,
        ServiceParameterKey.URL.value: ServiceURL.OPENAI.value,
        ServiceParameterKey.API_URL.value: ServiceURL.OPENAI.value,
    }


ServiceUnion = Union[
    ServiceID,
    ServiceParameterKey,
    ServiceConfigParameterKey,
    ServiceName,
    ServiceURL,
    ServiceModel,
    ServiceModelTypeTextEmbedding,
    ServiceModelTypeTextCompletion,
]


def get_service_static(static: Type[ServiceUnion], key: ServiceUnion) -> ServiceUnion:
    return static.__members__[key.name]
