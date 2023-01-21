import argparse
import sys

from mindflow.command_helpers.diff.diff import generate_diff_prompt
from mindflow.client.mindflow.completion import completion as remote_completion
from mindflow.utils.args import _add_diff_args, _add_response_args
from mindflow.utils.response import handle_response_text


class Diff:
    skip_clipboard: bool
    return_prompt: bool
    diffargs: str

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Prompt GPT model with git diff.",
        )
        _add_diff_args(parser)
        _add_response_args(parser)

        args = parser.parse_args(sys.argv[2:])
        self.diffargs = args.diffargs
        self.return_prompt = True
        self.skip_clipboard = args.skip_clipboard

    def execute(self):
        """
        This function is used to generate a git diff and then use it as a prompt for GPT bot.
        """
        # Run Git diff and get the output with prompt suffix
        prompt = generate_diff_prompt(self.diffargs)

        ## Prompt GPT through Mindflow API
        response: str = remote_completion(prompt, self.return_prompt).text

        handle_response_text(response, self.skip_clipboard)
