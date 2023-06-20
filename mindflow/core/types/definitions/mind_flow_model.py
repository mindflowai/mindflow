from enum import Enum

from mindflow.core.types.definitions.model import ModelID
from mindflow.core.types.definitions.model_type import ModelType


class MindFlowModelParameterKey(Enum):
    ID = "id"
    NAME = "name"
    DEFAULTS = "defaults"
    DESCRIPTION = "description"


class MindFlowModelID(Enum):
    QUERY = "query"
    INDEX = "index"
    EMBEDDING = "embedding"


class MindFlowModelDefaults(Enum):
    QUERY: dict = {
        "openai": ModelID.GPT_3_5_TURBO.value,
    }
    INDEX: dict = {
        "openai": ModelID.GPT_3_5_TURBO.value,
    }
    EMBEDDING: dict = {
        "openai": ModelID.TEXT_EMBEDDING_ADA_002.value,
    }


class MindFlowModelName(Enum):
    QUERY = "Query"
    INDEX = "Index"
    EMBEDDING = "Embedding"


class MindFlowModelType(Enum):
    QUERY = ModelType.TEXT_COMPLETION.value
    INDEX = ModelType.TEXT_COMPLETION.value
    EMBEDDING = ModelType.TEXT_EMBEDDING.value


class MindFlowModelDescription(Enum):
    QUERY = f"{MindFlowModelName.QUERY}:    Used to respond to chat, queries, and git functionality."
    INDEX = f"{MindFlowModelName.INDEX}:    Used to generate index summaries used for search."
    EMBEDDING = f"{MindFlowModelName.EMBEDDING}:    Used to generate embeddings for text used in search."


MINDFLOW_MODEL_STATIC = {
    MindFlowModelID.QUERY.value: {
        MindFlowModelParameterKey.ID.value: MindFlowModelID.QUERY.value,
        MindFlowModelParameterKey.NAME.value: MindFlowModelName.QUERY.value,
        MindFlowModelParameterKey.DEFAULTS.value: MindFlowModelDefaults.QUERY.value,
        MindFlowModelParameterKey.DESCRIPTION.value: MindFlowModelDescription.QUERY.value,
    },
    MindFlowModelID.INDEX.value: {
        MindFlowModelParameterKey.ID.value: MindFlowModelID.INDEX.value,
        MindFlowModelParameterKey.NAME.value: MindFlowModelName.INDEX.value,
        MindFlowModelParameterKey.DEFAULTS.value: MindFlowModelDefaults.INDEX.value,
        MindFlowModelParameterKey.DESCRIPTION.value: MindFlowModelDescription.INDEX.value,
    },
    MindFlowModelID.EMBEDDING.value: {
        MindFlowModelParameterKey.ID.value: MindFlowModelID.EMBEDDING.value,
        MindFlowModelParameterKey.NAME.value: MindFlowModelName.EMBEDDING.value,
        MindFlowModelParameterKey.DEFAULTS.value: MindFlowModelDefaults.EMBEDDING.value,
        MindFlowModelParameterKey.DESCRIPTION.value: MindFlowModelDescription.EMBEDDING.value,
    },
}
