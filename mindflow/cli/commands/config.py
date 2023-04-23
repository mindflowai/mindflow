import sys
from typing import List
import click
from mindflow.db.db.json import JSON_DATABASE
from mindflow.db.objects.mindflow_model import (
    MindFlowModel,
    MindFlowModelConfig,
    MindFlowModelID,
)

from mindflow.db.objects.static_definition.model import (
    ModelID,
)
from mindflow.db.objects.model import Model
from mindflow.db.utils import getOrCreateObject


@click.command(
    help="Configure MindFlow. For example, you can configure the model to use."
)
def config():
    config_options = ["model"]
    selected_config = select_option(
        "What do you want to configure? Enter #", config_options, config_options
    )
    if selected_config == "model":
        model_selection()

    JSON_DATABASE.save_file()


def model_selection():
    mindflow_model_ids = [
        MindFlowModelID.QUERY.value,
        MindFlowModelID.INDEX.value,
        MindFlowModelID.EMBEDDING.value,
    ]
    mindflow_model_options: List[MindFlowModel] = [
        MindFlowModel.load(mindflow_model_id)
        for mindflow_model_id in mindflow_model_ids
    ]
    mindflow_model_descriptions: List[str] = [
        mindflow_model.name for mindflow_model in mindflow_model_options
    ]

    selected_mindflow_model: MindFlowModel = select_option(
        "Select MindFlow model. Enter #",
        mindflow_model_options,
        mindflow_model_descriptions,
    )
    if selected_mindflow_model.id == MindFlowModelID.QUERY.value:
        query_model_selection()
    elif selected_mindflow_model.id == MindFlowModelID.INDEX.value:
        index_model_selection()
    elif selected_mindflow_model.id == MindFlowModelID.EMBEDDING.value:
        embedding_model_selection()


def query_model_selection():
    model_ids = [
        ModelID.GPT_3_5_TURBO.value,
        ModelID.GPT_4.value,
        ModelID.CLAUDE_INSTANT_V1.value,
        ModelID.CLAUDE_V1.value,
    ]
    model_options: List[Model] = [Model.load(model_id) for model_id in model_ids]
    model_descriptions: List[str] = [
        model.config_description for model in model_options
    ]

    selected_model: Model = select_option(
        "Select chat model. Recommended GPT-4/Claude V1. Enter #",
        model_options,
        model_descriptions,
    )

    mindflow_model_config: MindFlowModelConfig = getOrCreateObject(
        MindFlowModelConfig, f"{MindFlowModelID.QUERY.value}_config"
    )
    mindflow_model_config.model = selected_model.id
    mindflow_model_config.save()

    print(f"Query Model: {selected_model.id} saved!")


def index_model_selection():
    model_ids = [
        ModelID.GPT_3_5_TURBO.value,
        ModelID.GPT_4.value,
        ModelID.CLAUDE_INSTANT_V1.value,
        ModelID.CLAUDE_V1.value,
    ]
    model_options: List[Model] = [Model.load(model_id) for model_id in model_ids]
    model_descriptions: List[str] = [
        model.config_description for model in model_options
    ]

    selected_model: Model = select_option(
        "Select chat model. Recommended GPT-3.5 Turbo/Claude Instant V1. Enter #",
        model_options,
        model_descriptions,
    )
    mindflow_model_config: MindFlowModelConfig = getOrCreateObject(
        MindFlowModelConfig, f"{MindFlowModelID.INDEX.value}_config"
    )
    mindflow_model_config.model = selected_model.id
    mindflow_model_config.save()

    print(f"Index Model: {selected_model.id} saved!")


def embedding_model_selection():
    model_ids = [ModelID.TEXT_EMBEDDING_ADA_002.value]
    model_options: List[Model] = [Model.load(model_id) for model_id in model_ids]
    model_descriptions: List[str] = [
        model.config_description for model in model_options
    ]

    selected_model: Model = select_option(
        "Select chat model. Only one option... for now :) Enter #",
        model_options,
        model_descriptions,
    )

    mindflow_model_config: MindFlowModelConfig = getOrCreateObject(
        MindFlowModelConfig, f"{MindFlowModelID.EMBEDDING.value}_config"
    )
    mindflow_model_config.model = selected_model.id
    mindflow_model_config.save()

    print(f"Embedding Model: {selected_model.id} saved!")


def clear_console(lines: int):
    for _ in range(lines):
        sys.stdout.write("\033[F")  # Move cursor up one line
        sys.stdout.write("\033[K")  # Clear the line


# Takes a prompt and a list of descriptions and returns the index of the selected description
def select_option(prompt: str, options: List, descriptions: List[str]) -> int:
    # Print options with numbers
    for i, description in enumerate(descriptions, 1):
        click.echo(f"{i}: {description}")

    # Validate input and adjust index for 0-based list
    lines_to_clear = len(descriptions)
    while True:
        selected_option_index = click.prompt(prompt, type=int)
        lines_to_clear += 1
        if 1 <= selected_option_index <= len(descriptions):
            break
        click.echo("Invalid selection. Please try again.")
        lines_to_clear += 1

    clear_console(lines_to_clear)
    return options[selected_option_index - 1]
