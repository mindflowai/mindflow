"""
Send basic prompts to the backend.
"""

import requests
from mindflow.utils.config import Config


class PromptRequest:
    """
    Prompt request object.
    """

    prompt: str = None
    return_prompt: bool = None
    auth: str = None

    def __init__(self, prompt: str, return_prompt: bool, auth: str):
        self.prompt = prompt
        self.return_prompt = return_prompt
        self.auth = auth


class PromptResponse:
    """
    Prompt response object.
    """

    text: str = None

    def __init__(self, response: dict):
        self.text = response["text"]


def request_prompt(prompt: str, return_prompt: bool = False) -> PromptResponse:
    """
    This function makes a post request to the backend to get a direct response from GPT.
    """
    response = requests.post(
        f"{Config.API_LOCATION}/prompt",
        json=vars(PromptRequest(prompt, return_prompt, Config.AUTH)),
        timeout=10,
    )
    if response.status_code != 200:
        raise ValueError(f"Error: {response.status_code} {response.text}")
    return PromptResponse(response.json())
