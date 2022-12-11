"""
This file is used to load the chat gpt model.
"""

import json
import os

from revChatGPT.revChatGPT import Chatbot


def get_chat_gpt():
    """
    Get the chat gpt model.
    """
    path = os.environ["CHAT_GPT_CONFIG_FILE_PATH"]
    with open(path, "r", encoding="utf-8") as file:
        config = json.load(file)

    try:
        model = Chatbot(config)
    except ValueError as e:
        if hasattr(e, "message"):
            print(e.message)
        print("\n\nChat GPT API Failure occured. If using a session token, it may have expired so try updating it.")

    return model
