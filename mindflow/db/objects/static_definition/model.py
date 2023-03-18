from mindflow.db.objects.static_definition.model_type import ModelType
from mindflow.utils.enum import ExtendedEnum


class ModelID(ExtendedEnum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"

    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_32K = "gpt-4-32k"
    GPT_4_32K_0314 = "gpt-4-32k-0314"

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
    CONFIG_DESCRIPTION = "config_description"


class ModelService(ExtendedEnum):
    GPT_3_5_TURBO = "openai"
    GPT_3_5_TURBO_0301 = "openai"

    GPT_4 = "openai"
    GPT_4_0314 = "openai"
    GPT_4_32K = "openai"
    GPT_4_32K_0314 = "openai"

    TEXT_EMBEDDING_ADA_002 = "openai"


class ModelConfigParameterKey(ExtendedEnum):
    SOFT_TOKEN_LIMIT = "soft_token_limit"


class ModelConfigParameterName(ExtendedEnum):
    SOFT_TOKEN_LIMIT = "Soft Token Limit"


class ModelName(ExtendedEnum):
    GPT_3_5_TURBO = "GPT 3.5 Turbo"
    GPT_3_5_TURBO_0301 = "GPT 3.5 Turbo March 1st"

    GPT_4 = "GPT 4"
    GPT_4_0314 = "GPT 4 March 14th"
    GPT_4_32K = "GPT 4 32K"
    GPT_4_32K_0314 = "GPT 4 32K March 14th"

    TEXT_EMBEDDING_ADA_002 = "Text Embedding Ada 002"


class ModelSoftTokenLimit(ExtendedEnum):
    GPT_3_5_TURBO = 500
    GPT_3_5_TURBO_0301 = 500

    GPT_4 = 500
    GPT_4_0314 = 500
    GPT_4_32K = 500
    GPT_4_32K_0314 = 500

    TEXT_EMBEDDING_ADA_002 = 8191


class ModelHardTokenLimit(ExtendedEnum):
    GPT_3_5_TURBO = 4000
    GPT_3_5_TURBO_0301 = 4000

    GPT_4 = 8192
    GPT_4_0314 = 8192
    GPT_4_32K = 32_768
    GPT_4_32K_0314 = 32_768

    TEXT_EMBEDDING_ADA_002 = 8191


class ModelTokenCost(ExtendedEnum):
    GPT_3_5_TURBO = 0.002
    GPT_3_5_TURBO_0301 = 0.002

    GPT_4 = 0.002
    GPT_4_0314 = 0.002
    GPT_4_32K = 0.002
    GPT_4_32K_0314 = 0.002

    TEXT_EMBEDDING_ADA_002 = 0.0004


class ModelTokenCostUnit(ExtendedEnum):
    THOUSAND = 1000


class ModelDescription(ExtendedEnum):
    GPT_3_5_TURBO = f"GPT 3.5 Turbo: {str(ModelHardTokenLimit.GPT_3_5_TURBO.value)} token Limit. ${str(ModelTokenCost.GPT_3_5_TURBO.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    GPT_3_5_TURBO_0301 = f"GPT 3.5 Turbo March 1st: {str(ModelHardTokenLimit.GPT_3_5_TURBO_0301.value)} token Limit. ${str(ModelTokenCost.GPT_3_5_TURBO_0301.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."

    GPT_4 = f"GPT 4: {str(ModelHardTokenLimit.GPT_4.value)} token Limit. ${str(ModelTokenCost.GPT_4.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    GPT_4_0314 = f"GPT 4 March 14th: {str(ModelHardTokenLimit.GPT_4_0314.value)} token Limit. ${str(ModelTokenCost.GPT_4_0314.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    GPT_4_32K = f"GPT 4 32K: {str(ModelHardTokenLimit.GPT_4_32K.value)} token Limit. ${str(ModelTokenCost.GPT_4_32K.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."
    GPT_4_32K_0314 = f"GPT 4 32K March 14th: {str(ModelHardTokenLimit.GPT_4_32K_0314.value)} token Limit. ${str(ModelTokenCost.GPT_4_32K_0314.value)} per {str(ModelTokenCostUnit.THOUSAND.value)} tokens.     OpenAI's most powerful model. Longer outputs, more coherent, and more creative."

    TEXT_EMBEDDING_ADA_002 = f"Text Embedding Ada 002: {str(ModelHardTokenLimit.TEXT_EMBEDDING_ADA_002)} token Limit. ${str(ModelTokenCost.TEXT_EMBEDDING_ADA_002)} per {str(ModelTokenCostUnit.THOUSAND)} tokens.   OpenAI's best advertised embedding model. Fast and cheap! Recommended for generating deep and shallow indexes"


class ModelConfigDescription(ExtendedEnum):
    GPT_3_5_TURBO = f"{ModelName.GPT_3_5_TURBO.value}: Fast, cheap, and powerful.    Token Limit: {str(ModelHardTokenLimit.GPT_3_5_TURBO.value)}."
    GPT_4 = f"{ModelName.GPT_4.value}:         Most powerful model (slower). Token Limit: {str(ModelHardTokenLimit.GPT_4.value)}. Get access -> https://openai.com/waitlist/gpt-4-api."


## Service Models (By Type)
class ModelTextCompletionOpenAI(ExtendedEnum):
    GPT_3_5_TURBO = ModelID.GPT_3_5_TURBO.value
    GPT_3_5_TURBO_0301 = ModelID.GPT_3_5_TURBO_0301.value

    GPT_4 = ModelID.GPT_4.value
    GPT_4_0314 = ModelID.GPT_4_0314.value
    GPT_4_32K = ModelID.GPT_4_32K.value
    GPT_4_32K_0314 = ModelID.GPT_4_32K_0314.value


class ModelTextEmbeddingOpenAI(ExtendedEnum):
    TEXT_EMBEDDING_ADA_002 = ModelID.TEXT_EMBEDDING_ADA_002.value


## Service Models (ALL)
class ModelOpenAI(ExtendedEnum):
    GPT_3_5_TURBO = ModelID.GPT_3_5_TURBO.value
    GPT_3_5_TURBO_0301 = ModelID.GPT_3_5_TURBO_0301.value

    GPT_4 = ModelID.GPT_4.value
    GPT_4_0314 = ModelID.GPT_4_0314.value
    GPT_4_32K = ModelID.GPT_4_32K.value
    GPT_4_32K_0314 = ModelID.GPT_4_32K_0314.value

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
        ModelParameterKey.CONFIG_DESCRIPTION.value: ModelConfigDescription.GPT_3_5_TURBO.value,
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
    ModelID.GPT_4.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4.value,
        ModelParameterKey.NAME.value: ModelName.GPT_4.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_4.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_4.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_4.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_4.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
        ModelParameterKey.CONFIG_DESCRIPTION.value: ModelConfigDescription.GPT_4.value,
    },
    ModelID.GPT_4_0314.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4_0314.value,
        ModelParameterKey.NAME.value: ModelName.GPT_4_0314.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_4_0314.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_4_0314.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_4_0314.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_4_0314.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    },
    ModelID.GPT_4_32K.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4_32K.value,
        ModelParameterKey.NAME.value: ModelName.GPT_4_32K.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_4_32K.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_4_32K.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_4_32K.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_4_32K.value,
        ModelParameterKey.TOKEN_COST_UNIT.value: ModelTokenCostUnit.THOUSAND.value,
    },
    ModelID.GPT_4_32K_0314.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4_32K_0314.value,
        ModelParameterKey.NAME.value: ModelName.GPT_4_32K_0314.value,
        ModelParameterKey.SERVICE.value: ModelService.GPT_4_32K_0314.value,
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.SOFT_TOKEN_LIMIT.value: ModelSoftTokenLimit.GPT_4_32K_0314.value,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: ModelHardTokenLimit.GPT_4_32K_0314.value,
        ModelParameterKey.TOKEN_COST.value: ModelTokenCost.GPT_4_32K_0314.value,
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
