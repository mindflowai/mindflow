from enum import Enum

from mindflow.core.types.definitions.model_type import ModelType


class ModelParameterKey(Enum):
    ID = "id"
    NAME = "name"
    SERVICE = "service"
    MODEL_TYPE = "model_type"
    URL = "url"
    DEFAULT_SOFT_TOKEN_LIMIT = "default_soft_token_limit"
    HARD_TOKEN_LIMIT = "hard_token_limit"
    MAX_REQUESTS_PER_MINUTE = "max_requests_per_minute"
    MAX_TOKENS_PER_MINUTE = "max_tokens_per_minute"
    TOKEN_COST = "token_cost"
    TOKEN_COST_UNIT = "token_cost_unit"
    DESCRIPTION = "description"
    CONFIG_DESCRIPTION = "config_description"


class ModelConfigParameterKey(Enum):
    SOFT_TOKEN_LIMIT = "soft_token_limit"


class ModelID(Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    GPT_3_5_TURBO_0301 = "gpt-3.5-turbo-0301"

    GPT_4 = "gpt-4"
    GPT_4_0314 = "gpt-4-0314"
    GPT_4_32K = "gpt-4-32k"
    GPT_4_32K_0314 = "gpt-4-32k-0314"

    CLAUDE_V1 = "claude-v1"
    CLAUDE_V1_2 = "claude-v1.2"
    CLAUDE_INSTANT_V1 = "claude-instant-v1"

    TEXT_EMBEDDING_ADA_002 = "text-embedding-ada-002"


MODEL_STATIC: dict = {
    ModelID.GPT_3_5_TURBO.value: {
        ModelParameterKey.ID.value: ModelID.GPT_3_5_TURBO.value,
        ModelParameterKey.NAME.value: "GPT 3.5 Turbo",
        ModelParameterKey.SERVICE.value: "openai",
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.URL.value: "https://api.openai.com/v1/chat/completions",
        ModelParameterKey.DEFAULT_SOFT_TOKEN_LIMIT.value: 500,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: 4_000,
        ModelParameterKey.MAX_REQUESTS_PER_MINUTE.value: 3_500,
        ModelParameterKey.MAX_TOKENS_PER_MINUTE.value: 90_000,
        ModelParameterKey.TOKEN_COST.value: 0.002,
        ModelParameterKey.TOKEN_COST_UNIT.value: 1_000,
        ModelParameterKey.CONFIG_DESCRIPTION.value: f"GPT 3.5 Turbo:       OpenAI's Fast, cheap, and still powerful model.       Token Limit: {4_000}.",
    },
    ModelID.GPT_3_5_TURBO_0301.value: {
        ModelParameterKey.ID.value: ModelID.GPT_3_5_TURBO_0301.value,
        ModelParameterKey.NAME.value: "GPT 3.5 Turbo March 1st",
        ModelParameterKey.SERVICE.value: "openai",
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.URL.value: "https://api.openai.com/v1/chat/completions",
        ModelParameterKey.DEFAULT_SOFT_TOKEN_LIMIT.value: 500,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: 4_000,
        ModelParameterKey.MAX_REQUESTS_PER_MINUTE.value: 3_500,
        ModelParameterKey.MAX_TOKENS_PER_MINUTE.value: 90_000,
        ModelParameterKey.TOKEN_COST.value: 0.002,
        ModelParameterKey.TOKEN_COST_UNIT.value: 1_000,
    },
    ModelID.GPT_4.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4.value,
        ModelParameterKey.NAME.value: "GPT 4",
        ModelParameterKey.SERVICE.value: "openai",
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.URL.value: "https://api.openai.com/v1/chat/completions",
        ModelParameterKey.DEFAULT_SOFT_TOKEN_LIMIT.value: 500,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: 8_192,
        ModelParameterKey.MAX_REQUESTS_PER_MINUTE.value: 3_500,
        ModelParameterKey.MAX_TOKENS_PER_MINUTE.value: 90_000,
        ModelParameterKey.TOKEN_COST.value: 0.002,
        ModelParameterKey.TOKEN_COST_UNIT.value: 1_000,
        ModelParameterKey.CONFIG_DESCRIPTION.value: f"GPT 4:               OpenAI's most powerful model (slower + expensive).    Token Limit: {str(8192)}. Get access -> https://openai.com/waitlist/gpt-4-api.",
    },
    ModelID.GPT_4_0314.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4_0314.value,
        ModelParameterKey.NAME.value: "GPT 4 32K March 14th",
        ModelParameterKey.SERVICE.value: "openai",
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.URL.value: "https://api.openai.com/v1/chat/completions",
        ModelParameterKey.DEFAULT_SOFT_TOKEN_LIMIT.value: 500,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: 8_192,
        ModelParameterKey.MAX_REQUESTS_PER_MINUTE.value: 3_500,
        ModelParameterKey.MAX_TOKENS_PER_MINUTE.value: 90_000,
        ModelParameterKey.TOKEN_COST.value: 0.002,
        ModelParameterKey.TOKEN_COST_UNIT.value: 1_000,
    },
    ModelID.GPT_4_32K.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4_32K.value,
        ModelParameterKey.NAME.value: "GPT 4 32K",
        ModelParameterKey.SERVICE.value: "openai",
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.URL.value: "https://api.openai.com/v1/chat/completions",
        ModelParameterKey.DEFAULT_SOFT_TOKEN_LIMIT.value: 500,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: 32_768,
        ModelParameterKey.MAX_REQUESTS_PER_MINUTE.value: 3_500,
        ModelParameterKey.MAX_TOKENS_PER_MINUTE.value: 90_000,
        ModelParameterKey.TOKEN_COST.value: 0.002,
        ModelParameterKey.TOKEN_COST_UNIT.value: 1_000,
    },
    ModelID.GPT_4_32K_0314.value: {
        ModelParameterKey.ID.value: ModelID.GPT_4_32K_0314.value,
        ModelParameterKey.NAME.value: "GPT 4 32K March 14th",
        ModelParameterKey.SERVICE.value: "openai",
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.URL.value: "https://api.openai.com/v1/chat/completions",
        ModelParameterKey.DEFAULT_SOFT_TOKEN_LIMIT.value: 500,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: 32_768,
        ModelParameterKey.MAX_REQUESTS_PER_MINUTE.value: 3_500,
        ModelParameterKey.MAX_TOKENS_PER_MINUTE.value: 90_000,
        ModelParameterKey.TOKEN_COST.value: 0.002,
        ModelParameterKey.TOKEN_COST_UNIT.value: 1_000,
    },
    ModelID.TEXT_EMBEDDING_ADA_002.value: {
        ModelParameterKey.ID.value: ModelID.TEXT_EMBEDDING_ADA_002.value,
        ModelParameterKey.NAME.value: "Text Embedding Ada 002",
        ModelParameterKey.SERVICE.value: "openai",
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_EMBEDDING.value,
        ModelParameterKey.URL.value: "https://api.openai.com/v1/embeddings",
        ModelParameterKey.DEFAULT_SOFT_TOKEN_LIMIT.value: 500,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: 8_191,
        ModelParameterKey.MAX_REQUESTS_PER_MINUTE.value: 3_500,
        ModelParameterKey.MAX_TOKENS_PER_MINUTE.value: 350_000,
        ModelParameterKey.TOKEN_COST.value: 0.0004,
        ModelParameterKey.TOKEN_COST_UNIT.value: 1_000,
        ModelParameterKey.CONFIG_DESCRIPTION.value: f"Text Embedding Ada 002:   OpenAI's best and cheapest embedding model.    Token Limit: {str(8_191)}",
    },
    ModelID.CLAUDE_V1.value: {
        ModelParameterKey.ID.value: ModelID.CLAUDE_V1.value,
        ModelParameterKey.NAME.value: "Claude V1",
        ModelParameterKey.SERVICE.value: "anthropic",
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.URL.value: "",
        ModelParameterKey.DEFAULT_SOFT_TOKEN_LIMIT.value: 500,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: 9_000,
        ModelParameterKey.MAX_REQUESTS_PER_MINUTE.value: 0,
        ModelParameterKey.MAX_TOKENS_PER_MINUTE.value: 0,
        ModelParameterKey.TOKEN_COST.value: 2.90,
        ModelParameterKey.TOKEN_COST_UNIT.value: 1_000_000,
        ModelParameterKey.CONFIG_DESCRIPTION.value: f"Claude V1:           Anthropic's most powerful model (slower + expensive). Token Limit: {str(9_000)}. Get access -> https://www.anthropic.com/earlyaccess",
    },
    ModelID.CLAUDE_INSTANT_V1.value: {
        ModelParameterKey.ID.value: ModelID.CLAUDE_INSTANT_V1.value,
        ModelParameterKey.NAME.value: "Claude Instant V1",
        ModelParameterKey.SERVICE.value: "anthropic",
        ModelParameterKey.MODEL_TYPE.value: ModelType.TEXT_COMPLETION.value,
        ModelParameterKey.URL.value: "",
        ModelParameterKey.DEFAULT_SOFT_TOKEN_LIMIT.value: 500,
        ModelParameterKey.HARD_TOKEN_LIMIT.value: 9_000,
        ModelParameterKey.MAX_REQUESTS_PER_MINUTE.value: 0,
        ModelParameterKey.MAX_TOKENS_PER_MINUTE.value: 0,
        ModelParameterKey.TOKEN_COST.value: 0.43,
        ModelParameterKey.TOKEN_COST_UNIT.value: 1_000_000,
        ModelParameterKey.CONFIG_DESCRIPTION.value: f"Claude Instant V1:   Anthropic's Fast, cheap, and still powerful model.    Token Limit: {str(9_000)}. Get access -> https://www.anthropic.com/earlyaccess",
    },
}


## Service Models (ALL)
class ModelOpenAI(Enum):
    GPT_3_5_TURBO = ModelID.GPT_3_5_TURBO.value
    GPT_3_5_TURBO_0301 = ModelID.GPT_3_5_TURBO_0301.value

    GPT_4 = ModelID.GPT_4.value
    GPT_4_0314 = ModelID.GPT_4_0314.value
    GPT_4_32K = ModelID.GPT_4_32K.value
    GPT_4_32K_0314 = ModelID.GPT_4_32K_0314.value

    TEXT_EMBEDDING_ADA_002 = ModelID.TEXT_EMBEDDING_ADA_002.value


class ModelAnthropic(Enum):
    CLAUDE_V1 = ModelID.CLAUDE_V1.value
    CLAUDE_INSTANT_V1 = ModelID.CLAUDE_INSTANT_V1.value


## Service Models (By Type)
class ModelTextCompletionOpenAI(Enum):
    GPT_3_5_TURBO = ModelID.GPT_3_5_TURBO.value
    GPT_3_5_TURBO_0301 = ModelID.GPT_3_5_TURBO_0301.value

    GPT_4 = ModelID.GPT_4.value
    GPT_4_0314 = ModelID.GPT_4_0314.value
    GPT_4_32K = ModelID.GPT_4_32K.value
    GPT_4_32K_0314 = ModelID.GPT_4_32K_0314.value


class ModelTextCompletionAnthropic(Enum):
    CLAUDE_V1 = ModelID.CLAUDE_V1.value
    CLAUDE_INSTANT_V1 = ModelID.CLAUDE_INSTANT_V1.value


class ModelTextEmbeddingOpenAI(Enum):
    TEXT_EMBEDDING_ADA_002 = ModelID.TEXT_EMBEDDING_ADA_002.value
