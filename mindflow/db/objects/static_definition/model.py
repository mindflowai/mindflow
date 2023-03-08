from mindflow.db.objects.static_definition.model_type import ModelType
from mindflow.utils.enum import ExtendedEnum


class ModelID(ExtendedEnum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"

    # TEXT_DAVINCI_003 = "text-davinci-003"
    # TEXT_CURIE_001 = "text-curie-001"
    # TEXT_BABBAGE_001 = "text-babbage-001"
    # TEXT_ADA_001 = "text-ada-001"

    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"


class ModelParameterKey(ExtendedEnum):
    ID = "id"
    NAME = "name"
    SERVICE = "service"
    MODEL_TYPE = "model_type"
    SOFT_TOKEN_LIMIT = "soft_token_limit"
    HARD_TOKEN_LIMIT = "hard_token_limit"
    TOKEN_COST = "token_cost"
    TOKEN_COST_UNIT = "token_cost_unit"
    DESCRIPTION = "description"


class ModelService(ExtendedEnum):
    GPT_3_5_TURBO = "openai"
    GPT_3_5_TURBO_0301 = "openai"

    # TEXT_DAVINCI_003 = "openai"
    # TEXT_CURIE_001 = "openai"
    # TEXT_BABBAGE_001 = "openai"
    # TEXT_ADA_001 = "openai"

    TEXT_EMBEDDING_ADA_002 = "openai"


class ModelConfigParameterKey(ExtendedEnum):
    SOFT_TOKEN_LIMIT = "soft_token_limit"


class ModelConfigParameterName(ExtendedEnum):
    SOFT_TOKEN_LIMIT = "Soft Token Limit"


class ModelName(ExtendedEnum):
    GPT_3_5_TURBO = "GPT 3.5 Turbo"
    GPT_3_5_TURBO_0301 = "GPT 3.5 Turbo March 1st"

    # TEXT_DAVINCI_003 = "Text Davinci 003"
    # TEXT_CURIE_001 = "Text Curie 001"
    # TEXT_BABBAGE_001 = "Text Babbage 001"
    # TEXT_ADA_001 = "Text Ada 001"

    TEXT_EMBEDDING_ADA_002 = "Text Embedding Ada 002"


class ModelSoftTokenLimit(ExtendedEnum):
    GPT_3_5_TURBO = 500
    GPT_3_5_TURBO_0301 = 500

    # TEXT_DAVINCI_003 = 800
    # TEXT_CURIE_001 = 500
    # TEXT_BABBAGE_001 = 500
    # TEXT_ADA_001 = 500
    TEXT_EMBEDDING_ADA_002 = 8191


class ModelHardTokenLimit(ExtendedEnum):
    GPT_3_5_TURBO = 4000
    GPT_3_5_TURBO_0301 = 4000

    # TEXT_DAVINCI_003 = 4000
    # TEXT_CURIE_001 = 2048
    # TEXT_BABBAGE_001 = 2048
    # TEXT_ADA_001 = 2048
    TEXT_EMBEDDING_ADA_002 = 8191


class ModelTokenCost(ExtendedEnum):
    GPT_3_5_TURBO = 0.002
    GPT_3_5_TURBO_0301 = 0.002

    # TEXT_DAVINCI_003 = 0.02
    # TEXT_CURIE_001 = 0.002
    # TEXT_BABBAGE_001 = 0.0005
    # TEXT_ADA_001 = 0.0004

    TEXT_EMBEDDING_ADA_002 = 0.0004


class ModelTokenCostUnit(ExtendedEnum):
    THOUSAND = 1000


class ModelDescription(ExtendedEnum):
    GPT_3_5_TURBO = f"GPT 3.5 Turbo: {str(ModelHardTokenLimit.GPT_3_5_TURBO.value)} token Limit. ${str(ModelTokenCost.GPT_3_5_TURBO.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    GPT_3_5_TURBO_0301 = f"GPT 3.5 Turbo March 1st: {str(ModelHardTokenLimit.GPT_3_5_TURBO_0301.value)} token Limit. ${str(ModelTokenCost.GPT_3_5_TURBO_0301.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."

    # TEXT_DAVINCI_003 = f"Text Davinci 003: {str(ModelHardTokenLimit.TEXT_DAVINCI_003.value)} token Limit. ${str(ModelTokenCost.TEXT_DAVINCI_003.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    # TEXT_CURIE_001 = f"Text Curie 001:   {str(ModelHardTokenLimit.TEXT_CURIE_001.value)} token Limit. ${str(ModelTokenCost.TEXT_CURIE_001.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.    Very capable, but faster and lower cost than Davinci."
    # TEXT_BABBAGE_001 = f"Text Babbage 001: {str(ModelHardTokenLimit.TEXT_BABBAGE_001.value)} token Limit. ${str(ModelTokenCost.TEXT_BABBAGE_001.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.   Faster yet. Lower cost, but less compelling responses."
    # TEXT_ADA_001 = f"Text Ada 001:     {str(ModelHardTokenLimit.TEXT_ADA_001.value)} token Limit. ${str(ModelTokenCost.TEXT_ADA_001.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.   OpenAI's fasted and cheap model. Not recommended for generating final responses."

    TEXT_EMBEDDING_ADA_002 = f"Text Embedding Ada 002: {str(ModelHardTokenLimit.TEXT_EMBEDDING_ADA_002)} token Limit. ${str(ModelTokenCost.TEXT_EMBEDDING_ADA_002)} per {str(ModelTokenCostUnit.THOUSAND)} tokens.   OpenAI's best advertised embedding model. Fast and cheap! Recommended for generating deep and shallow indexes"


## Service Models (By Type)


class ModelTextCompletionOpenAI(ExtendedEnum):
    GPT_3_5_TURBO = ModelID.GPT_3_5_TURBO.value
    GPT_3_5_TURBO_0301 = ModelID.GPT_3_5_TURBO_0301.value

    # TEXT_DAVINCI_003 = ModelID.TEXT_DAVINCI_003.value
    # TEXT_CURIE_001 = ModelID.TEXT_CURIE_001.value
    # TEXT_BABBAGE_001 = ModelID.TEXT_BABBAGE_001.value
    # TEXT_ADA_001 = ModelID.TEXT_ADA_001.value


class ModelTextEmbeddingOpenAI(ExtendedEnum):
    TEXT_EMBEDDING_ADA_002 = ModelID.TEXT_EMBEDDING_ADA_002.value


## Service Models (ALL)


class ModelOpenAI(ExtendedEnum):
    GPT_3_5_TURBO = ModelID.GPT_3_5_TURBO.value
    GPT_3_5_TURBO_0301 = ModelID.GPT_3_5_TURBO_0301.value

    # TEXT_DAVINCI_003 = ModelID.TEXT_DAVINCI_003.value
    # TEXT_CURIE_001 = ModelID.TEXT_CURIE_001.value
    # TEXT_BABBAGE_001 = ModelID.TEXT_BABBAGE_001.value
    # TEXT_ADA_001 = ModelID.TEXT_ADA_001.value

    TEXT_EMBEDDING_ADA_002 = ModelID.TEXT_EMBEDDING_ADA_002.value


MODEL_STATIC: dict = {
    ModelID.GPT_3_5_TURBO.value: {
        ModelParameterKey.ID.value: ModelID.GPT_3_5_TURBO.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_3_5_TURBO.value,
        ModelParameterKey.NAME.value: ModelName.GPT_3_5_TURBO.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_3_5_TURBO.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_3_5_TURBO.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_3_5_TURBO.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    },
    ModelID.GPT_3_5_TURBO_0301.value: {
        ModelParameterKey.ID.value: ModelID.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.NAME.value: ModelName.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    },
    ModelID.TEXT_EMBEDDING_ADA_002.value: {
        ModelParameterKey.ID.value: ModelID.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.NAME.value: ModelName.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.SERVICE.value: ModelService.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_EMBEDDING.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    },
}


# ModelUnion = Union[
#     ModelID,
#     ModelParameterKey,
#     ModelName,
#     ModelHardTokenLimit,
#     ModelDescription,
# ]


# def get_model_static(static: Type[ModelUnion], key: ModelUnion) -> ModelUnion:
#     return static.__members__[key.name]
