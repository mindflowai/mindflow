import sys
from typing import List

from mindflow.db.objects.document import Document
from mindflow.db.objects.model import ConfiguredModel


def print_total_size(document_references: List[Document]):
    """
    Print total size of documents
    """
    total_size = sum(
        [document_reference.size for document_reference in document_references]
    )
    print(f"Total content size: MB {total_size / 1024 / 1024:.2f}")


def print_total_tokens_and_ask_to_continue(
    documents: List[Document],
    completion_model: ConfiguredModel,
    usd_threshold: float = 0.5,
):
    """
    Print total tokens of documents
    """
    total_tokens = sum([document.tokens for document in documents])
    print(f"Total tokens: {total_tokens}")
    total_cost_usd: float = (
        total_tokens / float(completion_model.token_cost_unit)
    ) * completion_model.token_cost
    if total_cost_usd > usd_threshold:
        print(f"Total cost: ${total_cost_usd:.2f}")
        while True:
            user_input = input("Would you like to continue? (yes/no): ")
            if user_input.lower() in ["no", "n"]:
                sys.exit(0)
            elif user_input.lower() in ["yes", "y"]:
                break


def get_text_within_xml(text: str, tag: str) -> str:
    """
    Get xml from text
    """
    start_tag = f"<{tag}>"
    end_tag = f"</{tag}>"
    start_index = text.index(start_tag) + len(start_tag)
    end_index = text.index(end_tag)
    return text[start_index:end_index]
