import asyncio
import os
import click
from result import Result, Err

from mindflow.core.commands.gen import run_code_generation
from mindflow.core.settings import Settings
from mindflow.core.types.model import ModelApiCallError


@click.command(help="AI powered boilerplate code generation.")
@click.argument("output_path", type=str)
@click.argument("prompt", type=str)
def gen(output_path: str, prompt: str):
    if os.path.exists(output_path):
        click.confirm(
            f"The output path '{output_path}' already exists. Do you want to overwrite it?",
            abort=True,
        )
        os.remove(output_path)

    if len((output_path_dir := os.path.dirname(output_path))) > 0:
        os.makedirs(output_path_dir, exist_ok=True)

    code_generation_result: Result[str, ModelApiCallError] = asyncio.run(
        run_code_generation(Settings(), output_path, prompt)
    )
    if isinstance(code_generation_result, Err):
        click.echo(f"Code generation failed: {code_generation_result.value}")
        return

    with open(output_path, "w") as f:
        f.write(code_generation_result.value)

    click.echo(f"Code generation complete. Your code is ready to go at {output_path}!")
