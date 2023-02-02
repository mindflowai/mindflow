from mindflow.db.objects.static_definition.service import (
    ServiceConfigParameterKey,
    ServiceConfigParameterName,
    ServiceID,
    ServiceName,
)
from mindflow.cli.config.main import menu


def ask_service_authorization() -> ServiceID:
    choice = menu(ServiceName.values(), "Which service would you like to authorize?")
    return ServiceID[ServiceName(choice).name]


def ask_service() -> ServiceID:
    choice = menu(ServiceName.values(), "Please select a service:")
    return ServiceID[ServiceName(choice).name]


def ask_service_config() -> ServiceConfigParameterKey:
    choice = menu(
        ServiceConfigParameterName.values(), "Please select a service configuration:"
    )
    return ServiceConfigParameterKey[ServiceConfigParameterName(choice).name]
