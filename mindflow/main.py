# Description: This is the main file of the program.

from mindflow.command_line_client import CommandLineClient


def main():
    """
    This is the main function.
    """
    client = CommandLineClient()
    client.execute()
