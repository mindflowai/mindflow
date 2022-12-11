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
    model = Chatbot(login_credentials)
    return model
