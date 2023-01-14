import pyperclip

def handle_response_text(text: str, skip_clipboard: bool):
    if not skip_clipboard:
        try:
            pyperclip.copy(text)
            print("Response copied to clipboard!!!")
            return
        except Exception as e:
            raise Exception(f"Failed to copy to clipboard: {e}")
    print(text)
