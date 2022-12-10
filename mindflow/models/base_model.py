"""
Contains the base class for all models.
"""


class BaseModel:
    """
    Base class for all language models to inherit from.
    """

    def __init__(self, model_name: str):
        """
        Initialize the model.
        """
        self.model_name = model_name

    def get_response(self, text: str):
        """
        Get the chat response from the model.
        """

    def login(self):
        """
        Login to the model.
        """
