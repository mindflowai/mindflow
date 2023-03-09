from typing import List
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
