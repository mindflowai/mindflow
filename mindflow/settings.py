from mindflow.db.objects.mindflow_model import ConfiguredMindFlowModels
from mindflow.db.objects.service import ConfiguredServices


class Settings:
    services: ConfiguredServices
    mindflow_models: ConfiguredMindFlowModels

    def __init__(self):
        self.services = ConfiguredServices()
        self.mindflow_models = ConfiguredMindFlowModels(self.services)
