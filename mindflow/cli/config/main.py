import getpass
import sys

from mindflow.cli.config.menu import menu
from mindflow.db.objects.mindflow_model import MindFlowModelConfig
from mindflow.db.objects.model import ModelConfig
from mindflow.db.objects.service import ServiceConfig
from mindflow.db.objects.static_definition.model import (
    ModelConfigParameterKey,
    ModelHardTokenLimit,
    get_model_static,
)
from mindflow.db.objects.static_definition.mind_flow_model import (
    MindFlowModelID,
)

from mindflow.db.objects.static_definition.service import (
    ServiceConfigParameterKey,
    ServiceID,
)
from mindflow.cli.config.questions.common.enums import (
    MainOption,
    YesNo,
)
from mindflow.cli.config.questions.common.questions import (
    ask_another_config,
)
from mindflow.cli.config.questions.service.questions import (
    ask_service,
    ask_service_config,
)
from mindflow.cli.config.questions.model.questions import (
    ask_mind_flow_model_type,
    ask_model_by_service,
    ask_model_config,
    ask_model_text_completion_openai,
    ask_model_text_embedding_openai,
)
from mindflow.state import STATE


def set_configuration():
    option_choice = menu(
        MainOption.values(), "Which options would you like to configure?"
    )
    match MainOption(option_choice):
        # Auth Config
        case MainOption.AUTHORIZE:
            config_service()
        # Model Config
        case MainOption.MIND_FLOW_MODEL:
            config_mindflow_model()
        case MainOption.MODEL:
            config_model()

    match YesNo(ask_another_config()):
        case YesNo.YES:
            set_configuration()


def config_service():
    service_key = ask_service()
    service_config_param = ask_service_config()

    match service_config_param:
        case ServiceConfigParameterKey.API_KEY:
            value = getpass.getpass("API Key: ")
        case ServiceConfigParameterKey.API_SECRET:
            value = getpass.getpass("API Secret: ")
        case _:
            print("Unrecognized model config parameter")
            sys.exit(1)
    
    service_config = ServiceConfig.load(f"{service_key.value}_config")
    if not service_config:
        service_config = ServiceConfig(id=f"{service_key.value}_config")

    setattr(service_config, service_config_param.value, value)
    service_config.save()

def config_model():
    service_key = ask_service()
    model_key = ask_model_by_service(service_key)
    model_config_param = ask_model_config()

    match model_config_param:
        case ModelConfigParameterKey.SOFT_TOKEN_LIMIT:
            model_hard_token_limit = get_model_static(
                ModelHardTokenLimit, model_key
            ).value
            while True:
                value = input("Soft Token Limit: ")
                if not value.isdigit():
                    print("Soft token limit must be a number")
                    continue
                value = int(value)
                if value > model_hard_token_limit:
                    print("Soft token limit cannot be greater than hard token limit")
                else:
                    break
        case _:
            print("Unrecognized model config parameter")
            sys.exit(1)
    
    model_configs = ModelConfig.load(f"{model_key.value}_config")
    if not model_configs:
        model_configs = ModelConfig(id=f"{model_key.value}_config")
    
    setattr(model_configs, model_config_param.value, value)
    model_configs.save()


def config_mindflow_model():
    mindflow_model_key = ask_mind_flow_model_type()
    match mindflow_model_key:
        case MindFlowModelID.INDEX:
            match ask_service():
                case ServiceID.OPENAI:
                    value = ask_model_text_completion_openai().value
        case MindFlowModelID.QUERY:
            match ask_service():
                case ServiceID.OPENAI:
                    value = ask_model_text_completion_openai().value
        case MindFlowModelID.EMBEDDING:
            match ask_service():
                case ServiceID.OPENAI:
                    value = ask_model_text_embedding_openai().value
    

    mindflow_model_config = MindFlowModelConfig.load(f"{mindflow_model_key.value}_config")
    if not mindflow_model_config:
        mindflow_model_config = MindFlowModelConfig(id=f"{mindflow_model_key.value}_config")

    setattr(mindflow_model_config, "model", value)
    mindflow_model_config.save()
