"""
This module contains the get_response function, which is used to get a response
"""

import sys


def get_response(model, prompt):
    """
    This function is used to get a response from the chatbot.
    """
    try:
        print("Please wait for model to formulate its full response...")
        response = model.get_chat_response(prompt)
    except ValueError as error:
        print("Something went wrong!")
        print(error)
        sys.exit(1)

    # Erase the "Please wait" line when done waiting
    sys.stdout.write("\033[F\033[K")

    return response["message"]
