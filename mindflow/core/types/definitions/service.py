from enum import Enum

from mindflow.core.types.definitions.model import ModelID
from mindflow.core.types.definitions.model import (
    ModelOpenAI,
    ModelAnthropic,
    ModelTextCompletionOpenAI,
    ModelTextEmbeddingOpenAI,
    ModelTextCompletionAnthropic,
)


class ServiceID(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    PINECONE = "pinecone"


class ServiceConfigID(Enum):
    OPENAI = "openai_config"
    ANTHROPIC = "anthropic_config"
    PINECONE = "pinecone_config"


class ServiceParameterKey(Enum):
    ID = "id"
    NAME = "name"
    URL = "url"
    API_URL = "api_url"
    DEFAULT_INDEX_MODEL = "default_index_model"
    DEFAULT_QUERY_MODEL = "default_query_model"
    DEFAULT_EMBEDDING_MODEL = "default_embedding_model"


class ServiceConfigParameterKey(Enum):
    API_KEY = "api_key"
    API_SECRET = "api_secret"

    MODELS = "models"


class ServiceConfigParameterName(Enum):
    API_KEY = "API Key"
    API_SECRET = "API Secret"

    MODELS = "Models"


class ServiceName(Enum):
    OPENAI = "OpenAI"
    ANTHROPIC = "Anthropic"
    PINECONE = "Pinecone"


class ServiceURL(Enum):
    OPENAI = ""
    ANTHROPIC = ""
    PINECONE = ""


class ServiceAPIURL(Enum):
    OPENAI = ""
    ANTHROPIC = ""
    PINECONE = ""


class ServiceDefaultIndexModel(Enum):
    OPENAI = ModelID.GPT_3_5_TURBO.value
    ANTHROPIC = ModelID.CLAUDE_INSTANT_V1.value


class ServiceDefaultQueryModel(Enum):
    OPENAI = ModelID.GPT_3_5_TURBO.value
    ANTHROPIC = ModelID.CLAUDE_V1.value


class ServiceDefaultEmbeddingModel(Enum):
    OPENAI = ModelID.TEXT_EMBEDDING_ADA_002.value


## Service Model Types
class ServiceModelTypeTextEmbedding(Enum):
    OPENAI = ModelTextEmbeddingOpenAI


class ServiceModelTypeTextCompletion(Enum):
    OPENAI = ModelTextCompletionOpenAI
    ANTHROPIC = ModelTextCompletionAnthropic


class ServiceModel(Enum):
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
