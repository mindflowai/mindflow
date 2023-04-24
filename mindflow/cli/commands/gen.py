import click

from mindflow.core.gen import run_code_generation


@click.command(help="AI powered boilerplate code generation.")
@click.argument("output_path", type=str)
@click.argument("prompt", type=str)
def gen(output_path: str, prompt: str):
    print(run_code_generation(output_path, prompt))
