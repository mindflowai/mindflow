import requests
from mindflow.config import API_LOCATION

def get_response(prompt: str):
        """
        This function makes a post request to the backend to get a direct response from GPT.
        """
        response = requests.post(f"{API_LOCATION}/response", json={"prompt": prompt})
        if response.status_code != 200:
            raise ValueError(f"Error: {response.status_code} {response.text}")
        return response.json()['response']