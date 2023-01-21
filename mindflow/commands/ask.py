import sys
import argparse

from mindflow.client.mindflow.completion import completion as remote_completion
from mindflow.utils.args import _add_ask_args, _add_response_args
from mindflow.utils.response import handle_response_text


class Ask:
    skip_clipboard: bool
    return_prompt: bool
    prompt: str

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Prompt GPT model with basic request.",
        )
        _add_ask_args(parser)
        _add_response_args(parser)

        args = parser.parse_args(sys.argv[2:])
        self.skip_clipboard: bool = args.skip_clipboard
        self.return_prompt: bool = True
        self.prompt: str = args.prompt

    def execute(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        ## Prompt GPT through Mindflow API
        response: str = remote_completion(self.prompt, self.return_prompt).text

        handle_response_text(response, self.skip_clipboard)
