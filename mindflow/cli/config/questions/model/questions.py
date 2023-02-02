from mindflow.cli.config.menu import menu
from mindflow.db.objects.static_definition.mind_flow_model import (
    MindFlowModelID,
    MindFlowModelName,
)
from mindflow.db.objects.static_definition.model import (
    ModelConfigParameterKey,
    ModelConfigParameterName,
    ModelID,
    ModelName,
)
from mindflow.db.objects.static_definition.service import (
    ServiceID,
    ServiceModel,
    get_service_static,
)
from mindflow.db.objects.static_definition.service import (
    ModelTextCompletionOpenAI,
    ModelTextEmbeddingOpenAI,
)


def ask_mind_flow_model_type() -> MindFlowModelID:
    mindflow_type_choice = menu(
        MindFlowModelName.values(), "Which LLM request would you like to configure?"
    )
    return MindFlowModelID[MindFlowModelName(mindflow_type_choice).name]


def ask_model_text_completion_openai() -> ModelID:
    openAIModels = [ModelName[key].value for key in ModelTextCompletionOpenAI.keys()]
    model_choice = menu(openAIModels, "Please select text completion model:")
    return ModelID[ModelName(model_choice).name]


def ask_model_text_embedding_openai() -> ModelID:
    openAIModels = [ModelName[key].value for key in ModelTextEmbeddingOpenAI.keys()]
    model_choice = menu(openAIModels, "Please select text embedding model:")
    return ModelID[ModelName(model_choice).name]


def ask_model_config() -> ModelConfigParameterKey:
    choice = menu(
        ModelConfigParameterName.values(), "Please select a model configuration:"
    )
    return ModelConfigParameterKey[ModelConfigParameterName(choice).name]


def ask_model_by_service(service_key: ServiceID) -> ModelID:
    service_models = get_service_static(ServiceModel, service_key).value
    service_model_names = [ModelName[key].value for key in service_models.keys()]
    model_choice = menu(service_model_names, "Please select a model:")
    return ModelID[ModelName(model_choice).name]
