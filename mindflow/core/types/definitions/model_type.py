from enum import Enum


class ModelType(Enum):
    TEXT_COMPLETION = "text_completion"
    TEXT_EMBEDDING = "text_embedding"


class ModelTypeName(Enum):
    TEXT_COMPLETION = "Text Completion"
    TEXT_EMBEDDING = "Text Embedding"


## Service Model Types
class ModelTypeOpenAI(Enum):
    TEXT_COMPLETION = ModelType.TEXT_COMPLETION.value
    TEXT_EMBEDDING = ModelType.TEXT_EMBEDDING.value
