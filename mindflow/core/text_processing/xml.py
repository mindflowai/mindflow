def get_text_within_xml(text: str, tag: str) -> str:
    start_tag = f"<{tag}>"
    end_tag = f"</{tag}>"
    start_index = text.index(start_tag) + len(start_tag)
    end_index = text.index(end_tag)
    return text[start_index:end_index]
