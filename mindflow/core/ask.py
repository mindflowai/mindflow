from mindflow.settings import Settings
from mindflow.utils.response import handle_response_text


def run_ask(prompt: str) -> str:
    """
    This function is used to generate a prompt and then use it as a prompt for GPT bot.
    """
    settings = Settings()
    # Prompt GPT through Mindflow API or locally
    response: str = settings.mindflow_models.query.model([{"role": "system", "content": "You are a helpful virtual assistant responding to a users query using your general knowledge and the text provided below."}, {"role": "user", "content": prompt}])
    return response
