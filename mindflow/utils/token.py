"""
Authentication token helpers.
"""
import os
import getpass


def set_token(token: str):
    """
    This function is used to set the token for the user.
    """
    if token is None:
        token = getpass.getpass("Authorization Key: ")

    with open(
        os.path.join(os.path.expanduser("~"), ".mindflow"), "w", encoding="utf-8"
    ) as file:
        file.write(token)
        file.close()

    print("Token set successfully.")


def get_token() -> str:
    """
    This function is used to get the token for the user.
    """
    with open(
        os.path.join(os.path.expanduser("~"), ".mindflow"), "r", encoding="utf-8"
    ) as file:
        token = file.read()
        file.close()
    return token
