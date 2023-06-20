def is_valid_utf8(document_text: str) -> bool:
    try:
        document_text.encode("utf-8")
        return True
    except UnicodeDecodeError:
        return False
