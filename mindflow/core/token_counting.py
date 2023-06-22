import os
from typing import Dict, List
from mindflow.core.types.model import ConfiguredModel


def get_token_count_of_text_for_model(model: ConfiguredModel, text: str) -> int:
    try:
        return len(model.tokenizer.encode(text))
    except Exception:
        return len(text) // 3


def get_batch_token_count_of_text_for_model(
    model: ConfiguredModel, texts: List[str]
) -> int:
    try:
        return sum(len(encoding) for encoding in model.tokenizer.encode_batch(texts))
    except Exception:
        return sum(len(text) // 3 for text in texts)


def get_token_count_of_messages_for_model(
    messages: List[Dict[str, str]],
    model: ConfiguredModel,
):
    return get_token_count_of_text_for_model(
        model,
        "\n\n".join(
            [f"{message['role']}\n\n{message['content']}" for message in messages]
        ),
    )


def get_token_count_from_document_query_for_model(
    document_paths: List[str],
    query: str,
    model: ConfiguredModel,
    return_texts: bool = False,
):
    texts = [query]
    for document_path in document_paths:
        if os.path.isdir(document_path):
            raise NotImplementedError("Directory support not yet implemented.")

        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Could not find file at {document_path}")

        file_text = {open(document_path, "r").read()}
        texts.append(f"```{file_text}```")

    tokens = get_batch_token_count_of_text_for_model(model, texts)
    if return_texts:
        return tokens, texts
    return tokens
