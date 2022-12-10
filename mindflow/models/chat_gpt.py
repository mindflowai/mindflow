"""
This file is used to load the chat gpt model.
"""

import json
import os

from ChatGPT.src.revChatGPT.revChatGPT import Chatbot


def get_chat_gpt():
    """
    Get the chat gpt model.
    """
    path = os.environ["CHAT_GTP_CONFIG_FILE_PATH"]
    with open(path, "r", encoding="utf-8") as file:
        config = json.load(file)

    model = Chatbot(config)
    if "session_token" in config:
        model.refresh_session()

    return model
