import click
from mindflow.cli.commands.config import select_option

from mindflow.core.types.definitions.service import ServiceConfigID
from mindflow.core.types.service import ServiceConfig
from mindflow.core.types.store_traits.json import save_json_store


@click.command(help="Set your API Key")
def login():
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

    save_json_store()
