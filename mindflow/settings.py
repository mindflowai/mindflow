from mindflow.db.objects.mindflow_model import ConfiguredMindFlowModels
from mindflow.db.objects.model import ConfiguredModels
from mindflow.db.objects.service import ConfiguredServices


class Settings:
    services: ConfiguredServices
    models: ConfiguredModels
    mindflow_models: ConfiguredMindFlowModels

    def __init__(self):
        self.services = ConfiguredServices()
        self.models = ConfiguredModels()
        self.mindflow_models = ConfiguredMindFlowModels(self.services, self.models)
