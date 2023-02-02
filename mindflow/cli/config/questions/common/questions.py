from mindflow.cli.config.main import menu
from mindflow.cli.config.questions.common.enums import YesNo


def ask_another_config() -> YesNo:
    continue_choice = menu(YesNo.values(), "Would you like to configure another item?")
    return YesNo(continue_choice)
