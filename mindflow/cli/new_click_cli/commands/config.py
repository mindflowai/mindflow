import click
from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.objects.mindflow_model import MindFlowModelConfig, MindFlowModelID

from mindflow.db.objects.static_definition.model import (
    MODEL_STATIC,
    ModelID,
    ModelName,
    ModelParameterKey,
)


@click.command(
    help="Configure MindFlow. For example, you can configure the model to use."
)
def config():
    config_options = ["model"]

    # Print configuration options with numbers
    for i, option in enumerate(config_options, 1):
        click.echo(f"{i}: {option}")

    selected_config_index = click.prompt(
        "What do you want to configure? Enter #", type=int
    )

    if 1 <= selected_config_index <= len(config_options):
        selected_config = config_options[selected_config_index - 1]

        if selected_config == "model":
            model_selection()
    else:
        click.echo("Invalid selection. Please try again.")

    DATABASE_CONTROLLER.databases.json.save_file()


def model_selection():
    model_options = [
        MODEL_STATIC[ModelID.GPT_3_5_TURBO.value],
        MODEL_STATIC[ModelID.GPT_4.value],
    ]
    options = [
        model[ModelParameterKey.CONFIG_DESCRIPTION.value] for model in model_options
    ]

    # Print options with numbers
    for i, option in enumerate(options, 1):
        click.echo(f"{i}: {option}")

    # Validate input and adjust index for 0-based list
    while True:
        selected_option_index = click.prompt("Select chat model. Enter #", type=int)
        if 1 <= selected_option_index <= len(options):
            break
        click.echo("Invalid selection. Please try again.")

    selected_model = model_options[selected_option_index - 1]
    mindflow_model_config = MindFlowModelConfig(f"{MindFlowModelID.QUERY.value}_config")

    if mindflow_model_config is None:
        mindflow_model_config = MindFlowModelConfig(
            f"{MindFlowModelID.QUERY.value}_config"
        )
    mindflow_model_config.model = selected_model[ModelParameterKey.ID.value]

    mindflow_model_config.save()
