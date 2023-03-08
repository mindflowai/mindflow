from mindflow.settings import Settings
from mindflow.utils.prompts import CHAT_PROMPT_PREFIX
from mindflow.utils.token import get_token_count


def run_chat(prompt: str) -> str:
    """
    This function is used to generate a prompt and then use it as a prompt for GPT bot.
    """
    settings = Settings()
    completion_model = settings.mindflow_models.query.model

    if (
        get_token_count(completion_model, CHAT_PROMPT_PREFIX + prompt)
        > completion_model.hard_token_limit
    ):
        print("The prompt is too long. Please try again with a shorter prompt.")
        return ""

    # Prompt GPT through Mindflow API or locally
    response: str = completion_model(
        [
            {
                "role": "system",
                "content": CHAT_PROMPT_PREFIX,
            },
            {"role": "user", "content": prompt},
        ]
    )
    return response
