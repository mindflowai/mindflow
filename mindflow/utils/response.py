"""
This module contains the get_response function, which is used to get a response
"""

import sys
from time import sleep


def progressively_trim_response(
    model, 
    prompt, 
    max_retries: int=5, 
    percent_left_after_trim: float = 0.5,
    sleep_seconds: float = 0,
):
    # trim the prompt length with each failure to at least try to get a response
    for _ in range(max_retries):
        try:
            response = model.get_chat_response(prompt)
            return response

        except Exception:
            # NOTE! THIS IS A HACK!!! IT'S TERRIBLE!

            # IMPORTANT NOTE: THIS TRIMS THE END OF THE PROMPT,
            # SO MAKE SURE YOU PLACE THE PROMPT PREFIX AT THE BEGINNING AND NOT THE END!

            assert percent_left_after_trim < 1 and percent_left_after_trim > 0
            max_characters = max(10, int(len(prompt) * percent_left_after_trim))
            print(f"Failed to get response, trimming prompt length from {len(prompt)} to {max_characters}")
            prompt = prompt[:max_characters]

            if sleep_seconds > 0:
                sleep(sleep_seconds)

    raise ValueError("Failed to get response.")


def get_response(model, prompt, max_retries: int = 5):
    """
    This function is used to get a response from the chatbot.
    """
    try:
        print("Please wait for model to formulate its full response...")
        response = progressively_trim_response(model, prompt, max_retries=max_retries)
    except ValueError as error:
        print("Something went wrong!")
        print(error)
        sys.exit(1)

    # Erase the "Please wait" line when done waiting
    sys.stdout.write("\033[F\033[K")

    return response["message"]
