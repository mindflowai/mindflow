import os
import click

from mindflow.core.convo import Conversation


CODE_GEN_SYSTEM_PROMPT = "All responses must be valid code for the specified language. Do not use any special characters or symbols, any additional information must be put in comments."


def run_code_generation(output_path: str, prompt: str):
    if os.path.exists(output_path):
        click.confirm(
            f"The output path '{output_path}' already exists. Do you want to overwrite it?",
            abort=True,
        )
        os.remove(output_path)

    output_path_dir = os.path.dirname(output_path)
    if len(output_path_dir) > 0:
        os.makedirs(output_path_dir, exist_ok=True)

    convo = Conversation(conversation_id="code_gen_0", system_prompt="")

    message = f"Generate code for '{output_path}' with the following prompt: '{prompt}'. Do NOT use any special characters or symbols, any additional information must be put in comments."

    convo.add_message(message)
    response = convo.get_response()

    parse_and_save_response(response, output_path)

    return f"Code generation complete. Your code is ready to go at {output_path}!"


def parse_and_save_response(response: str, output_path: str):
    # take the response and parse it into a valid file.

    with open(output_path, "w") as f:
        f.write(response)
