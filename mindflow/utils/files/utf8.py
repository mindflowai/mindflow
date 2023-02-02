"""
Quick UTF-8 validation.
"""


def is_valid_utf8(document_text: str) -> bool:
    """
    Check if a file is valid utf8.
    """
    try:
        document_text.encode("utf-8")
        return True
    except UnicodeDecodeError:
        return False
