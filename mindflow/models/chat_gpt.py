"""
This file is used to load the chat gpt model.
"""

import json
import os

from revChatGPT.revChatGPT import Chatbot


def get_chat_gpt(login_credentials):
    """
    Get the chat gpt model.
    """

    try:
        return Chatbot(login_credentials)
    except ValueError as e:
        if hasattr(e, "message"):
            print(e.message)
        print("\n\nChat GPT API Failure occured. If using a session token, it may have expired so try updating it.")
        exit(1)