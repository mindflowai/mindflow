from mindflow.db.objects.static_definition.model import ModelID
from mindflow.db.objects.static_definition.model import ModelOpenAI
from mindflow.db.objects.static_definition.model import ModelTextCompletionOpenAI
from mindflow.db.objects.static_definition.model import ModelTextEmbeddingOpenAI
from mindflow.utils.enum import ExtendedEnum


class ServiceID(ExtendedEnum):
    OPENAI = "openai"


class ServiceParameterKey(ExtendedEnum):
    ID = "id"
    NAME = "name"
    URL = "url"
    API_URL = "api_url"
    DEFAULT_INDEX_MODEL = "default_index_model"
    DEFAULT_QUERY_MODEL = "default_query_model"
    DEFAULT_EMBEDDING_MODEL = "default_embedding_model"


class ServiceConfigParameterKey(ExtendedEnum):
    API_KEY = "api_key"
    API_SECRET = "api_secret"

    MODELS = "models"


class ServiceConfigParameterName(ExtendedEnum):
    API_KEY = "API Key"
    API_SECRET = "API Secret"

    MODELS = "Models"


class ServiceName(ExtendedEnum):
    OPENAI = "OpenAI"


class ServiceURL(ExtendedEnum):
    OPENAI = ""


class ServiceAPIURL(ExtendedEnum):
    OPENAI = ""


class ServiceDefaultIndexModel(ExtendedEnum):
    OPENAI = ModelID.GPT_3_5_TURBO.value


class ServiceDefaultQueryModel(ExtendedEnum):
    OPENAI = ModelID.GPT_3_5_TURBO.value


class ServiceDefaultEmbeddingModel(ExtendedEnum):
    OPENAI = ModelID.TEXT_EMBEDDING_ADA_002.value


## Service Model Types
class ServiceModelTypeTextEmbedding(ExtendedEnum):
    OPENAI = ModelTextEmbeddingOpenAI


class ServiceModelTypeTextCompletion(ExtendedEnum):
    OPENAI = ModelTextCompletionOpenAI


class ServiceModel(ExtendedEnum):
    OPENAI = ModelOpenAI


SERVICE_STATIC = {
    ServiceID.OPENAI.value: {
        ServiceParameterKey.ID.value: ServiceID.OPENAI.value,
        ServiceParameterKey.NAME.value: ServiceName.OPENAI.value,
        ServiceParameterKey.URL.value: ServiceURL.OPENAI.value,
        ServiceParameterKey.API_URL.value: ServiceURL.OPENAI.value,
        ServiceParameterKey.DEFAULT_INDEX_MODEL.value: ServiceDefaultIndexModel.OPENAI.value,
        ServiceParameterKey.DEFAULT_QUERY_MODEL.value: ServiceDefaultQueryModel.OPENAI.value,
        ServiceParameterKey.DEFAULT_EMBEDDING_MODEL.value: ServiceDefaultEmbeddingModel.OPENAI.value,
    },
}


# ServiceUnion = Union[
#     ServiceID,
#     ServiceParameterKey,
#     ServiceConfigParameterKey,
#     ServiceName,
#     ServiceURL,
#     ServiceModel,
#     ServiceModelTypeTextEmbedding,
#     ServiceModelTypeTextCompletion,
# ]


# def get_service_static(static: Type[ServiceUnion], key: ServiceUnion) -> ServiceUnion:
#     return static.__members__[key.name]
