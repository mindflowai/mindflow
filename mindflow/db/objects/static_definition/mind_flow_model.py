from mindflow.db.objects.static_definition.model import ModelID
from mindflow.db.objects.static_definition.model_type import ModelType
from mindflow.utils.enum import ExtendedEnum


class MindFlowModelParameterKey(ExtendedEnum):
    ID = "id"
    NAME = "name"
    DEFAULTS = "defaults"


class MindFlowModelID(ExtendedEnum):
    QUERY = "query"
    INDEX = "index"
    EMBEDDING = "embedding"


class MindFlowModelDefaults(ExtendedEnum):
    QUERY: dict = {
        "openai": ModelID.GPT_3_5_TURBO.value,
    }
    INDEX: dict = {
        "openai": ModelID.GPT_3_5_TURBO.value,
    }
    EMBEDDING: dict = {
        "openai": ModelID.TEXT_EMBEDDING_ADA_002.value,
    }


class MindFlowModelName(ExtendedEnum):
    QUERY = "Query"
    INDEX = "Index"
    EMBEDDING = "Embedding"


class MindFlowModelType(ExtendedEnum):
    QUERY = ModelType.TEXT_COMPLETION.value
    INDEX = ModelType.TEXT_COMPLETION.value
    EMBEDDING = ModelType.TEXT_EMBEDDING.value


class MindFlowModelDescription(ExtendedEnum):
    QUERY = f"{MindFlowModelName.QUERY}:    Used to generate final response from query."
    INDEX = f"{MindFlowModelName.INDEX}:    Used to generate deep index from query. (Warning! Expensive and slow!)"


MINDFLOW_MODEL_STATIC = {
    MindFlowModelID.QUERY.value: {
        MindFlowModelParameterKey.ID.value: MindFlowModelID.QUERY.value,
        MindFlowModelParameterKey.NAME.value: MindFlowModelName.QUERY.value,
        MindFlowModelParameterKey.DEFAULTS.value: MindFlowModelDefaults.QUERY.value,
    },
    MindFlowModelID.INDEX.value: {
        MindFlowModelParameterKey.ID.value: MindFlowModelID.INDEX.value,
        MindFlowModelParameterKey.NAME.value: MindFlowModelName.INDEX.value,
        MindFlowModelParameterKey.DEFAULTS.value: MindFlowModelDefaults.INDEX.value,
    },
    MindFlowModelID.EMBEDDING.value: {
        MindFlowModelParameterKey.ID.value: MindFlowModelID.EMBEDDING.value,
        MindFlowModelParameterKey.NAME.value: MindFlowModelName.EMBEDDING.value,
        MindFlowModelParameterKey.DEFAULTS.value: MindFlowModelDefaults.EMBEDDING.value,
    },
}

# MindFlowModelUnion = Union[
#     MindFlowModelID,
#     MindFlowModelDefaults,
#     MindFlowModelName,
#     MindFlowModelType,
#     MindFlowModelDescription,
# ]


# def get_mind_flow_model_static(
#     static: Type[MindFlowModelUnion], key: MindFlowModelUnion
# ) -> MindFlowModelUnion:
#     return static.__members__[key.name]
