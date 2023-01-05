import requests
from mindflow.config import Config

def request_prompt(prompt: str):
    """
    This function makes a post request to the backend to get a direct response from GPT.
    """
    response = requests.post(f"{Config.API_LOCATION}/prompt", json={"prompt": prompt, "auth": Config.AUTH})
    if response.status_code != 200:
        raise ValueError(f"Error: {response.status_code} {response.text}")
    return response.json()['text']
