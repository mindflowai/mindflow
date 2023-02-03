"""
`ask` command
"""

from mindflow.state import STATE
from mindflow.client.gpt import GPT
from mindflow.utils.response import handle_response_text


def ask():
    """
    This function is used to generate a prompt and then use it as a prompt for GPT bot.
    """
    # Prompt GPT through Mindflow API or locally
    response = GPT.query(STATE.arguments.query)
    handle_response_text(response)
