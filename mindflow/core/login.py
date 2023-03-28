from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.objects.service import ServiceConfig


def run_login():
    api_choice = input("Choose API to configure: \n1. OpenAI\n2. Anthropic\n")
    while api_choice not in ["1", "2"]:
        api_choice = input("Invalid choice. Please choose 1 or 2: ")

    api_key = input("Enter API key: ")
    service_config_id: str
    if api_choice == "1":
        service_config_id = "openai_config"
    else:
        service_config_id = "anthropic_config"

    service_config = ServiceConfig.load(service_config_id)
    if not service_config:
        service_config = ServiceConfig(service_config_id)

    service_config.api_key = api_key
    service_config.save()

    DATABASE_CONTROLLER.databases.json.save_file()
