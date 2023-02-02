from typing import Type, Union
from mindflow.db.objects.static_definition.model_type import ModelType
from mindflow.utils.enum import ExtendedEnum


class ModelID(ExtendedEnum):
    TEXT_DAVINCI_003 = "text_davinci_003"
    TEXT_CURIE_001 = "text_curie_001"
    TEXT_BABBAGE_001 = "text_babbage_001"
    TEXT_ADA_001 = "text_ada_001"

    TEXT_EMBEDDING_ADA_002 = "text_embedding_ada_002"


class ModelParameterKey(ExtendedEnum):
    ID = "id"
    API = "api"
    NAME = "name"
    MODEL_TYPE = "model_type"
    HARD_TOKEN_LIMIT = "hard_token_limit"
    TOKEN_COST = "token_cost"
    TOKEN_COST_UNIT = "token_cost_unit"
    DESCRIPTION = "description"


class ModelAPI(ExtendedEnum):
    TEXT_DAVINCI_003 = "text-davinci-003"
    TEXT_CURIE_001 = "text-curie-001"
    TEXT_BABBAGE_001 = "text-babbage-001"
    TEXT_ADA_001 = "text-ada-001"

    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"


class ModelConfigParameterKey(ExtendedEnum):
    SOFT_TOKEN_LIMIT = "soft_token_limit"


class ModelConfigParameterName(ExtendedEnum):
    SOFT_TOKEN_LIMIT = "Soft Token Limit"


class ModelName(ExtendedEnum):
    TEXT_DAVINCI_003 = "Text Davinci 003"
    TEXT_CURIE_001 = "Text Curie 001"
    TEXT_BABBAGE_001 = "Text Babbage 001"
    TEXT_ADA_001 = "Text Ada 001"

    TEXT_EMBEDDING_ADA_002 = "Text Embedding Ada 002"


class ModelHardTokenLimit(ExtendedEnum):
    TEXT_DAVINCI_003 = 4000
    TEXT_CURIE_001 = 2048
    TEXT_BABBAGE_001 = 2048
    TEXT_ADA_001 = 2048
    TEXT_EMBEDDING_ADA_002 = 8191


class ModelTokenCost(ExtendedEnum):
    TEXT_DAVINCI_003 = 0.02
    TEXT_CURIE_001 = 0.002
    TEXT_BABBAGE_001 = 0.0005
    TEXT_ADA_001 = 0.0004
    TEXT_EMBEDDING_ADA_002 = 0.0004


class ModelTokenCostUnit(ExtendedEnum):
    THOUSAND = 1000


class ModelDescription(ExtendedEnum):
    TEXT_DAVINCI_003 = f"Text Davinci 003: {str(ModelHardTokenLimit.TEXT_DAVINCI_003.value)} token Limit. ${str(ModelTokenCost.TEXT_DAVINCI_003.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    TEXT_CURIE_001 = f"Text Curie 001:   {str(ModelHardTokenLimit.TEXT_CURIE_001.value)} token Limit. ${str(ModelTokenCost.TEXT_CURIE_001.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.    Very capable, but faster and lower cost than Davinci."
    TEXT_BABBAGE_001 = f"Text Babbage 001: {str(ModelHardTokenLimit.TEXT_BABBAGE_001.value)} token Limit. ${str(ModelTokenCost.TEXT_BABBAGE_001.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.   Faster yet. Lower cost, but less compelling responses."
    TEXT_ADA_001 = f"Text Ada 001:     {str(ModelHardTokenLimit.TEXT_ADA_001.value)} token Limit. ${str(ModelTokenCost.TEXT_ADA_001.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.   OpenAI's fasted and cheap model. Not recommended for generating final responses."

    TEXT_EMBEDDING_ADA_002 = f"Text Embedding Ada 002: {str(ModelHardTokenLimit.TEXT_EMBEDDING_ADA_002)} token Limit. ${str(ModelTokenCost.TEXT_EMBEDDING_ADA_002)} per {str(ModelTokenCostUnit.THOUSAND)} tokens.   OpenAI's best advertised embedding model. Fast and cheap! Recommended for generating deep and shallow indexes"


## Service Models (By Type)


class ModelTextCompletionOpenAI(ExtendedEnum):
    TEXT_DAVINCI_003 = ModelID.TEXT_DAVINCI_003.value
    TEXT_CURIE_001 = ModelID.TEXT_CURIE_001.value
    TEXT_BABBAGE_001 = ModelID.TEXT_BABBAGE_001.value
    TEXT_ADA_001 = ModelID.TEXT_ADA_001.value


class ModelTextEmbeddingOpenAI(ExtendedEnum):
    TEXT_EMBEDDING_ADA_002 = ModelID.TEXT_EMBEDDING_ADA_002.value


## Service Models (ALL)


class ModelOpenAI(ExtendedEnum):
    TEXT_DAVINCI_003 = ModelID.TEXT_DAVINCI_003.value
    TEXT_CURIE_001 = ModelID.TEXT_CURIE_001.value
    TEXT_BABBAGE_001 = ModelID.TEXT_BABBAGE_001.value
    TEXT_ADA_001 = ModelID.TEXT_ADA_001.value

    TEXT_EMBEDDING_ADA_002 = ModelID.TEXT_EMBEDDING_ADA_002.value


class ModelStatic(ExtendedEnum):
    TEXT_DAVINCI_003: dict = {
        ModelParameterKey.ID.value: ModelID.TEXT_DAVINCI_003.value,
        ModelParameterKey.API.value: ModelAPI.TEXT_DAVINCI_003.value,
        ModelParameterKey.NAME.value: ModelName.TEXT_DAVINCI_003.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.TEXT_DAVINCI_003.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.TEXT_DAVINCI_003.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    }
    TEXT_CURIE_001: dict = {
        ModelParameterKey.ID.value: ModelID.TEXT_CURIE_001.value,
        ModelParameterKey.API.value: ModelAPI.TEXT_CURIE_001.value,
        ModelParameterKey.NAME.value: ModelName.TEXT_CURIE_001.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.TEXT_CURIE_001.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.TEXT_CURIE_001.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    }
    TEXT_BABBAGE_001: dict = {
        ModelParameterKey.ID.value: ModelID.TEXT_BABBAGE_001.value,
        ModelParameterKey.API.value: ModelAPI.TEXT_BABBAGE_001.value,
        ModelParameterKey.NAME.value: ModelName.TEXT_BABBAGE_001.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.TEXT_BABBAGE_001.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.TEXT_BABBAGE_001.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    }
    TEXT_ADA_001: dict = {
        ModelParameterKey.ID.value: ModelID.TEXT_ADA_001.value,
        ModelParameterKey.API.value: ModelAPI.TEXT_ADA_001.value,
        ModelParameterKey.NAME.value: ModelName.TEXT_ADA_001.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.TEXT_ADA_001.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.TEXT_ADA_001.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    }

    TEXT_EMBEDDING_ADA_002: dict = {
        ModelParameterKey.ID.value: ModelID.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.API.value: ModelAPI.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.NAME.value: ModelName.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_EMBEDDING.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    }


ModelUnion = Union[
    ModelID,
    ModelStatic,
    ModelParameterKey,
    ModelName,
    ModelHardTokenLimit,
    ModelDescription,
]


def get_model_static(static: Type[ModelUnion], key: ModelUnion) -> ModelUnion:
    return static.__members__[key.name]
