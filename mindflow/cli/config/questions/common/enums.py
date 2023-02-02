from mindflow.utils.enum import ExtendedEnum


class MainOption(ExtendedEnum):
    AUTHORIZE = "authorize a service"
    MIND_FLOW_MODEL = "select model for use by MindFlow"
    MODEL = "configure a model"


class YesNo(ExtendedEnum):
    YES = "Yes"
    NO = "No"
