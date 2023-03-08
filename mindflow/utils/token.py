from typing import List
from mindflow.db.objects.model import ConfiguredModel


def get_token_count(model: ConfiguredModel, text: str) -> int:
    """
    This function is used to get the token count of a string.
    """
    return len(model.tokenizer.encode(text))

def get_batch_token_count(model: ConfiguredModel, texts: List[str]) -> int:
    """
    This function is used to get the token count of a list of strings.
    """
    return sum([len(encoding) for encoding in model.tokenizer.encode_batch(texts)])