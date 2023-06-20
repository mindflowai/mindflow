from concurrent.futures import ThreadPoolExecutor
import hashlib
import sys

from typing import List, Optional, TypeVar

from alive_progress import alive_bar
import numpy as np

from mindflow.core.types.document import (
    Document,
    DocumentChunk,
    DocumentReference,
    get_document_id,
)
from mindflow.core.types.model import ConfiguredModel
from mindflow.core.types.document import read_document
from mindflow.core.resolving.resolve import resolve_paths_to_document_references
from mindflow.core.settings import Settings
from mindflow.core.prompt_builders import (
    Role,
    build_prompt_from_conversation_messages,
    create_conversation_message,
)
from mindflow.core.prompts import INDEX_PROMPT_PREFIX
from mindflow.core.token_counting import get_token_count_of_text_for_model


def run_index(document_paths: List[str]) -> str:
    settings = Settings()
    completion_model: ConfiguredModel = settings.mindflow_models.index.model
    embedding_model: ConfiguredModel = settings.mindflow_models.embedding.model

    document_references: List[DocumentReference] = resolve_paths_to_document_references(
        document_paths
    )

    if not (
        indexable_documents := get_indexable_documents(
            document_references, completion_model
        )
    ):  
        return "No documents to index"

    print_total_size_of_documents(indexable_documents)
    print_total_tokens_and_ask_to_continue(indexable_documents, completion_model)

    index_documents(indexable_documents, completion_model, embedding_model)

    return "Successfully indexed documents"


def print_total_size_of_documents(documents: List[Document]):
    print(
        f"Total content size: MB {sum([document.size for document in documents]) / 1024 / 1024:.2f}"
    )


def print_total_tokens_and_ask_to_continue(
    documents: List[Document],
    completion_model: ConfiguredModel,
    usd_threshold: float = 0.5,
):
    total_tokens = sum([document.tokens for document in documents])
    print(f"Total tokens: {total_tokens}")
    total_cost_usd: float = (
        total_tokens / float(completion_model.token_cost_unit)
    ) * completion_model.token_cost
    if total_cost_usd > usd_threshold:
        print(f"Total cost: ${total_cost_usd:.2f}")
        while True:
            if (
                user_input := input("Would you like to continue? (yes/no): ").lower()
            ) in ["no", "n"]:
                sys.exit(0)
            elif user_input in ["yes", "y"]:
                break
            else:
                print("Invalid input. Please try again.")


def index_documents(
    documents: List[Document],
    completion_model: ConfiguredModel,
    embedding_model: ConfiguredModel,
) -> None:
    with alive_bar(len(documents), bar="blocks", spinner="twirls") as progress_bar:
        with ThreadPoolExecutor(max_workers=50) as executor:
            document_chunk_futures = [
                executor.submit(
                    split_document_to_chunks_by_token_count_and_generate_embeddings,
                    completion_model,
                    embedding_model,
                    indexable_document,
                )
                for indexable_document in documents
            ]

            for document, document_chunk_future in zip(
                documents, document_chunk_futures
            ):
                document_chunks = document_chunk_future.result()

                document.num_chunks = len(document_chunks)
                document.embedding = list(
                    np.mean(
                        [
                            document_chunk.embedding
                            for document_chunk in document_chunks
                        ],
                        axis=0,
                    )
                )

                DocumentChunk.save_bulk(document_chunks)
                document.save()

                progress_bar()


def get_indexable_documents(
    document_references: List[DocumentReference], completion_model: ConfiguredModel
) -> List[Document]:
    document_ids = [
        document_id
        for document_id in [
            get_document_id(document_reference.path, document_reference.document_type)
            for document_reference in document_references
        ]
        if document_id is not None
    ]
    documents: List[Optional[Document]] = Document.load_bulk(document_ids)
    return [
        indexable_document
        for document, document_reference in zip(documents, document_references)
        if (
            indexable_document := get_indexable_document(
                document, document_reference, completion_model
            )
        )
        is not None
    ]


def get_indexable_document(
    document: Optional[Document],
    document_reference: DocumentReference,
    completion_model: ConfiguredModel,
) -> Optional[Document]:
    if not (
        document_text := read_document(
            document_reference.path, document_reference.document_type
        )
    ):
        return None

    document_text_bytes = document_text.encode("utf-8")
    document_hash = hashlib.sha256(document_text_bytes).hexdigest()

    if document and document.id == document_hash:
        return None

    return Document(
        {
            "id": document_hash,
            "path": document_reference.path,
            "document_type": document_reference.document_type,
            "num_chunks": document.num_chunks if document else 0,
            "size": len(document_text_bytes),
            "tokens": get_token_count_of_text_for_model(
                completion_model, document_text
            ),
        }
    )


def split_document_to_chunks_by_token_count_and_generate_embeddings(
    completion_model: ConfiguredModel,
    embedding_model: ConfiguredModel,
    indexable_document: Document,
) -> List[DocumentChunk]:
    if not (
        text := read_document(indexable_document.path, indexable_document.document_type)
    ):
        print("Document staged for indexing could not be read")
        sys.exit(1)

    if (
        token_count := get_token_count_of_text_for_model(completion_model, text)
    ) < completion_model.soft_token_limit:
        return [
            process_small_document(
                completion_model,
                embedding_model,
                text,
                indexable_document.id,
                token_count,
            )
        ]

    return process_large_document(
        completion_model, embedding_model, text, indexable_document.id
    )


def process_small_document(
    completion_model: ConfiguredModel,
    embedding_model: ConfiguredModel,
    text: str,
    document_id: str,
    tokens: int,
) -> DocumentChunk:
    summary: str = completion_model(
        build_prompt_from_conversation_messages(
            [
                create_conversation_message(Role.SYSTEM.value, INDEX_PROMPT_PREFIX),
                create_conversation_message(Role.USER.value, text),
            ],
            completion_model,
        )
    )
    return DocumentChunk(
        {
            "id": f"{document_id}_0",
            "summary": summary,
            "embedding": embedding_model(summary),
            "start_pos": 0,
            "end_pos": len(text),
            "num_tokens": tokens,
        }
    )


def process_large_document(
    completion_model: ConfiguredModel,
    embedding_model: ConfiguredModel,
    text: str,
    document_id: str,
) -> List[DocumentChunk]:
    return collect_leaves_with_embeddings_from_appended_branch_summaries(
        create_hierarchical_summary_tree(
            split_raw_text_to_document_chunks(
                completion_model, embedding_model, text, document_id
            ),
            completion_model,
        ),
        "",
        embedding_model,
    )


def split_raw_text_to_document_chunks(
    completion_model: ConfiguredModel,
    embedding_model: ConfiguredModel,
    text: str,
    document_hash: str,
) -> List[DocumentChunk]:
    start = 0
    end = len(text)
    document_chunks: List[DocumentChunk] = []

    while start < end:
        text_chunk_size = binary_search_max_raw_text_chunk_size_for_token_limit(
            completion_model, text, start, end
        )

        text_str = text[start : start + text_chunk_size]
        summary: str = completion_model(
            build_prompt_from_conversation_messages(
                [
                    create_conversation_message(Role.SYSTEM.value, INDEX_PROMPT_PREFIX),
                    create_conversation_message(Role.USER.value, text_str),
                ],
                completion_model,
            )
        )
        document_chunks.append(
            DocumentChunk(
                {
                    "id": f"{document_hash}_{len(document_chunks)}",
                    "summary": summary,
                    "embedding": embedding_model(summary),
                    "start_pos": start,
                    "end_pos": start + text_chunk_size,
                    "num_tokens": get_token_count_of_text_for_model(
                        completion_model, text_str
                    ),
                }
            )
        )

        start += text_chunk_size

    return document_chunks


def binary_search_max_raw_text_chunk_size_for_token_limit(
    completion_model: ConfiguredModel, text: str, start: int, end: int
) -> int:
    left = 0
    right = end - start
    while left < right:
        mid = (left + right + 1) // 2
        if (
            get_token_count_of_text_for_model(
                completion_model, text[start : start + mid]
            )
            <= completion_model.soft_token_limit
        ):
            left = mid
        else:
            right = mid - 1
    return left


class Node:
    def __init__(self, id, summary, children=None):
        self.id = id
        self.summary = summary
        self.children: List[T] = children if children else []

    def __repr__(self):
        return (
            f"Node(id={self.id}, summary={self.summary}, children={len(self.children)})"
        )


T = TypeVar("T", Node, DocumentChunk)


def create_hierarchical_summary_tree(
    nodes: List[T], completion_model: ConfiguredModel
) -> Node:
    if (
        get_token_count_of_text_for_model(
            completion_model, (summary := " ".join(node.summary for node in nodes))
        )
        <= completion_model.soft_token_limit
    ):
        summary = " ".join(node.summary for node in nodes)
        node_id = f"parent_{nodes[0].id.split('_')[0]}"
        return Node(node_id, summary, nodes)

    mid = len(nodes) // 2
    left_tree = create_hierarchical_summary_tree(nodes[:mid], completion_model)
    right_tree = create_hierarchical_summary_tree(nodes[mid:], completion_model)

    merged_summary = completion_model(
        build_prompt_from_conversation_messages(
            [
                create_conversation_message(Role.SYSTEM.value, INDEX_PROMPT_PREFIX),
                create_conversation_message(
                    Role.USER.value, f"{left_tree.summary} {right_tree.summary}"
                ),
            ],
            completion_model,
        )
    )

    parent_id = f"parent_{left_tree.id.split('_')[1]}_{right_tree.id.split('_')[1]}"
    return Node(parent_id, merged_summary, [left_tree, right_tree])


def collect_leaves_with_embeddings_from_appended_branch_summaries(
    node: T,
    ancestor_summaries: str,
    embedding_model: ConfiguredModel,
) -> List[DocumentChunk]:
    if isinstance(node, DocumentChunk):
        node.embedding = embedding_model(f"{ancestor_summaries} {node.summary}")
        return [node]

    return [
        leaf
        for child in node.children
        for leaf in collect_leaves_with_embeddings_from_appended_branch_summaries(
            child, f"{ancestor_summaries} {node.summary}", embedding_model
        )
    ]
