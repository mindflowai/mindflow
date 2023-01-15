"""
Handle response text from Mindflow API.
"""

import pyperclip

def handle_response_text(text: str, skip_clipboard: bool):
    """
    Copy to clipboard or print response text.
    """
    if not skip_clipboard:
        try:
            pyperclip.copy(text)
            print("Response copied to clipboard!!!")
            return
        except Exception as error:
            raise Exception(f"Failed to copy to clipboard: {error}")
    print(text)
