from mindflow.db.objects.static_definition.model import ModelID
from mindflow.db.objects.static_definition.model import ModelOpenAI, ModelAnthropic
from mindflow.db.objects.static_definition.model import ModelTextCompletionOpenAI
from mindflow.db.objects.static_definition.model import ModelTextEmbeddingOpenAI
from mindflow.utils.enum import ExtendedEnum


class ServiceID(ExtendedEnum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    PINECONE = "pinecone"


class ServiceConfigID(ExtendedEnum):
    OPENAI = "openai_config"
    ANTHROPIC = "anthropic_config"
    PINECONE = "pinecone_config"


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
    ANTHROPIC = "Anthropic"
    PINECONE = "Pinecone"


class ServiceURL(ExtendedEnum):
    OPENAI = ""
    ANTHROPIC = ""
    PINECONE = ""


class ServiceAPIURL(ExtendedEnum):
    OPENAI = ""
    ANTHROPIC = ""
    PINECONE = ""


class ServiceDefaultIndexModel(ExtendedEnum):
    OPENAI = ModelID.GPT_3_5_TURBO.value
    ANTHROPIC = ModelID.CLAUDE_INSTANT_V1.value


class ServiceDefaultQueryModel(ExtendedEnum):
    OPENAI = ModelID.GPT_3_5_TURBO.value
    ANTHROPIC = ModelID.CLAUDE_V1.value


class ServiceDefaultEmbeddingModel(ExtendedEnum):
    OPENAI = ModelID.TEXT_EMBEDDING_ADA_002.value


## Service Model Types
class ServiceModelTypeTextEmbedding(ExtendedEnum):
    OPENAI = ModelTextEmbeddingOpenAI


class ServiceModelTypeTextCompletion(ExtendedEnum):
    OPENAI = ModelTextCompletionOpenAI
    ANTHROPIC = ModelTextCompletionOpenAI


class ServiceModel(ExtendedEnum):
    OPENAI = ModelOpenAI
    ANTHROPIC = ModelAnthropic


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
    ServiceID.ANTHROPIC.value: {
        ServiceParameterKey.ID.value: ServiceID.ANTHROPIC.value,
        ServiceParameterKey.NAME.value: ServiceName.ANTHROPIC.value,
        ServiceParameterKey.URL.value: ServiceURL.ANTHROPIC.value,
        ServiceParameterKey.API_URL.value: ServiceURL.ANTHROPIC.value,
        ServiceParameterKey.DEFAULT_INDEX_MODEL.value: ServiceDefaultIndexModel.ANTHROPIC.value,
        ServiceParameterKey.DEFAULT_QUERY_MODEL.value: ServiceDefaultQueryModel.ANTHROPIC.value,
    },
    ServiceID.PINECONE.value: {
        ServiceParameterKey.ID.value: ServiceID.PINECONE.value,
        ServiceParameterKey.NAME.value: ServiceName.PINECONE.value,
        ServiceParameterKey.URL.value: ServiceURL.PINECONE.value,
        ServiceParameterKey.API_URL.value: ServiceURL.PINECONE.value,
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
