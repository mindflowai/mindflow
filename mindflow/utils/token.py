import os
from typing import Dict, List
from mindflow.db.objects.model import ConfiguredModel


def get_token_count(model: ConfiguredModel, text: str) -> int:
    """
    This function is used to get the token count of a string.
    """
    try:
        return len(model.tokenizer.encode(text))
    except Exception:
        return len(text) // 3


def get_batch_token_count(model: ConfiguredModel, texts: List[str]) -> int:
    """
    This function is used to get the token count of a list of strings.
    """
    try:
        return sum([len(encoding) for encoding in model.tokenizer.encode_batch(texts)])
    except Exception:
        return sum([len(text) // 3 for text in texts])


def estimate_tokens_from_messages(
    messages: List[Dict[str, str]],
    model: ConfiguredModel,
):
    content = ""
    for i in range(len(messages)):
        content += f"{messages[i]['role']}\n\n {messages[i]['content']}"

    return get_token_count(model, content)


def estimate_tokens_from_paths(
    document_paths: List[str],
    query: str,
    model: ConfiguredModel,
    return_texts: bool = False,
):
    texts = [query]
    for document_path in document_paths:
        # check if directory
        if os.path.isdir(document_path):
            raise NotImplementedError("Directory support not yet implemented.")

        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Could not find file at {document_path}")

        file_text = {open(document_path, "r").read()}
        text = f"```{file_text}```"
        texts.append(text)

    tokens = get_batch_token_count(model, texts)
    if return_texts:
        return tokens, texts
    return tokens
