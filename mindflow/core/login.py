from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.objects.service import ServiceConfig


def run_login(openai_api_key):
    service_config = ServiceConfig.load("openai_config")
    if not service_config:
        service_config = ServiceConfig("openai_config")

    service_config.api_key = openai_api_key
    service_config.save()

    DATABASE_CONTROLLER.databases.json.save_file()
