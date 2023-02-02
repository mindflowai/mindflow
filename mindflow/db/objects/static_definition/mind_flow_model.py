from typing import Type, Union
from mindflow.db.objects.static_definition.model_type import ModelType
from mindflow.utils.enum import ExtendedEnum


class MindFlowModelID(ExtendedEnum):
    QUERY = "query"
    INDEX = "index"
    EMBEDDING = "embedding"


class MindFlowModelName(ExtendedEnum):
    QUERY = "Query"
    INDEX = "Index"
    EMBEDDING = "Embedding"


class MindflowModelType(ExtendedEnum):
    QUERY = ModelType.TEXT_COMPLETION.value
    INDEX = ModelType.TEXT_COMPLETION.value
    EMBEDDING = ModelType.TEXT_EMBEDDING.value


class MindFlowModelDescription(ExtendedEnum):
    QUERY = f"{MindFlowModelName.QUERY}:    Used to generate final response from query."
    INDEX = f"{MindFlowModelName.INDEX}:    Used to generate deep index from query. (Warning! Expensive and slow!)"


MindFlowModelUnion = Union[
    MindFlowModelID,
    MindFlowModelName,
    MindflowModelType,
    MindFlowModelDescription,
]


def get_mind_flow_model_static(
    static: Type[MindFlowModelUnion], key: MindFlowModelUnion
) -> MindFlowModelUnion:
    return static.__members__[key.name]
