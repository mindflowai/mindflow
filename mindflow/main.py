"""
Main
"""

from mindflow.cli import CommandLineInterface


def main():
    """
    This is the main function.
    """
    client = CommandLineInterface()
    client.execute()
