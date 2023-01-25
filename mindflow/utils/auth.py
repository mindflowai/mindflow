"""
Authentication token helpers.
"""
import os
import sys
import json
import getpass
from enum import Enum

from simple_term_menu import TerminalMenu

from mindflow import DOT_MINDFLOW


class AuthType(Enum):
    """
    Authorization type enum
    """

    MINDFLOW = "Mindflow"
    OPENAI = "OpenAI"


def set_token(token):
    """
    Set authorization token for user from AuthType enum.
    """
    auth_file_path = os.path.join(DOT_MINDFLOW, "authentication.json")

    # Ask user to select type of token
    options = list(AuthType.__members__.keys())
    print("Select the type of token you want to set:")
    menu = TerminalMenu(options)
    choice = menu.show()

    # Get the selected token type
    selected_token_type = options[choice]

    # Prompt user to set token if it is None
    if token is None:
        token = getpass.getpass("Authorization Key: ")

    if os.path.isfile(auth_file_path):
        # Open the authentication file in read and write mode
        with open(auth_file_path, "r+", encoding="utf-8") as auth_file:
            # Read the existing authentication data
            authentication = json.load(auth_file)
    else:
        authentication = {}

    # Write the token to authentication file
    authentication[selected_token_type] = token

    # Write the updated authentication data to the file
    with open(auth_file_path, "w", encoding="utf-8") as auth_file:
        json.dump(authentication, auth_file)

    print(f"{selected_token_type} token has been saved.")


def get_token(auth_type: AuthType) -> str:
    """
    This function is retrieve specified token from authentication file.
    """

    auth_file_path = os.path.join(DOT_MINDFLOW, "authentication.json")
    if os.path.isfile(auth_file_path):
        with open(auth_file_path, "r+", encoding="utf-8") as auth_file:
            authentication = json.load(auth_file)
    else:
        authentication = {}

    if not authentication.get(auth_type.value):
        print(
            f"Please set authentication token first for {auth_type.value} using 'mindflow auth' command."
        )
        sys.exit(1)

    return authentication[auth_type.value]
