import argparse
import sys


from mindflow.utils.args import _add_auth_args
from mindflow.utils.token import set_token


class Auth:
    token: str

    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Authorize User.",
        )
        _add_auth_args(parser)
        args = parser.parse_args(sys.argv[2:])

        self.token = args.token

    def execute(self):
        """
        Authenticate user with Mindflow or OpenAI token.
        """
        set_token(self.token)
