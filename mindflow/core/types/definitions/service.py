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


SERVICE_STATIC = {
    ServiceID.OPENAI.value: {
        ServiceParameterKey.ID.value: ServiceID.OPENAI.value,
        ServiceParameterKey.NAME.value: "OpenAI",
        ServiceParameterKey.URL.value: "https://api.openai.com",
        ServiceParameterKey.API_URL.value: "https://api.openai.com/v1/",
        ServiceParameterKey.DEFAULT_INDEX_MODEL.value: ModelID.GPT_3_5_TURBO.value,
        ServiceParameterKey.DEFAULT_QUERY_MODEL.value: ModelID.GPT_3_5_TURBO.value,
        ServiceParameterKey.DEFAULT_EMBEDDING_MODEL.value: ModelID.TEXT_EMBEDDING_ADA_002.value,
    },
    ServiceID.ANTHROPIC.value: {
        ServiceParameterKey.ID.value: ServiceID.ANTHROPIC.value,
        ServiceParameterKey.NAME.value: "Anthropic",
        ServiceParameterKey.URL.value: "",
        ServiceParameterKey.API_URL.value: "",
        ServiceParameterKey.DEFAULT_INDEX_MODEL.value: ModelID.CLAUDE_V1.value,
        ServiceParameterKey.DEFAULT_QUERY_MODEL.value: ModelID.CLAUDE_INSTANT_V1.value,
    },
    ServiceID.PINECONE.value: {
        ServiceParameterKey.ID.value: ServiceID.PINECONE.value,
        ServiceParameterKey.NAME.value: "Pinecone",
        ServiceParameterKey.URL.value: "",
        ServiceParameterKey.API_URL.value: "",
    },
}


## Service Model Types
class ServiceModelTypeTextEmbedding(Enum):
    OPENAI = ModelTextEmbeddingOpenAI


class ServiceModelTypeTextCompletion(Enum):
    OPENAI = ModelTextCompletionOpenAI
    ANTHROPIC = ModelTextCompletionAnthropic


class ServiceModel(Enum):
    OPENAI = ModelOpenAI
    ANTHROPIC = ModelAnthropic
