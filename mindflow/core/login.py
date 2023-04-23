from mindflow.cli.commands.config import select_option
from mindflow.db.db.json import JSON_DATABASE
from mindflow.db.objects.service import ServiceConfig
from mindflow.db.objects.static_definition.service import ServiceConfigID


def run_login():
    service_ids = [
        ServiceConfigID.OPENAI.value,
        ServiceConfigID.ANTHROPIC.value,
        ServiceConfigID.PINECONE.value,
    ]
    service_options = [
        ServiceConfig.load(service_id, False) for service_id in service_ids
    ]
    service_descriptions = ["OpenAI", "Anthropic", "Pinecone: (Vector DB)"]
    service_config: ServiceConfig = select_option(
        "Choose service to configure. Enter #",
        service_options,
        service_descriptions,
    )

    service_config.api_key = input("Enter API key: ")
    if service_config.id == ServiceConfigID.PINECONE.value:
        service_config.environment = input("Enter environment: ")

    service_config.save()

    JSON_DATABASE.save_file()
