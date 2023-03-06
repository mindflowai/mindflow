"""
Handle response text from Mindflow API.
"""

import pyperclip

from mindflow.state import STATE


def handle_response_text(text: str):
    """
    Copy to clipboard or print response text.
    """
    if not STATE.arguments.skip_clipboard:
        try:
            pyperclip.copy(f"\n{text}")
            print("Response copied to clipboard!!!")
            return
        except Exception:
            # raise Exception(f"Failed to copy to clipboard: {error}")
            pass
    print(text)
