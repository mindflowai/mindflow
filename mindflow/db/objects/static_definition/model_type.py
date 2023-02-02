from typing import Union
from mindflow.utils.enum import ExtendedEnum


class ModelType(ExtendedEnum):
    TEXT_COMPLETION = "text_completion"
    TEXT_EMBEDDING = "text_embedding"


class ModelTypeName(ExtendedEnum):
    TEXT_COMPLETION = "Text Completion"
    TEXT_EMBEDDING = "Text Embedding"


## Service Model Types
class ModelTypeOpenAI(ExtendedEnum):
    TEXT_COMPLETION = ModelType.TEXT_COMPLETION.value
    TEXT_EMBEDDING = ModelType.TEXT_EMBEDDING.value


ModelTypeUnion = Union[
    ModelType,
    ModelTypeName,
    ModelTypeOpenAI,
]


def get_model_type_static(
    static: ModelTypeUnion, key: ModelTypeUnion
) -> ModelTypeUnion:
    return static.__members__[key.name]
