"""
`index` command
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib

from typing import List, Optional, Tuple, TypeVar, Iterable

from alive_progress import alive_bar
import numpy as np

from mindflow.db.objects.document import Document, DocumentChunk, get_document_id
from mindflow.db.objects.document import read_document
from mindflow.db.objects.model import ConfiguredModel
from mindflow.resolving.resolve import resolve_all
from mindflow.settings import Settings
from mindflow.utils.helpers import (
    print_total_size,
    print_total_tokens_and_ask_to_continue,
)
from mindflow.utils.prompt_builders import Role, build_prompt, create_message
from mindflow.utils.prompts import INDEX_PROMPT_PREFIX
from mindflow.utils.token import get_token_count


def run_index(document_paths: List[str], refresh: bool, verbose: bool = True) -> None:
    """
    This function is used to generate an index and/or embeddings for files
    """
    settings = Settings()
    completion_model: ConfiguredModel = settings.mindflow_models.index.model
    embedding_model: ConfiguredModel = settings.mindflow_models.embedding.model

    ## Resolve documents to document references
    resolved: List[Tuple[str, str]] = resolve_all(document_paths)
    indexable_documents: List[Document] = get_indexable_documents(
        resolved, completion_model
    )

    if not indexable_documents:
        if verbose:
            print("No documents to index")
        return

    print_total_size(indexable_documents)
    print_total_tokens_and_ask_to_continue(indexable_documents, completion_model)

    # build search trees in parallel
    with alive_bar(
        len(indexable_documents), bar="blocks", spinner="twirls"
    ) as progress_bar:
        with ThreadPoolExecutor(max_workers=50) as executor:
            document_chunk_futures = [
                executor.submit(
                    create_document_chunks,
                    completion_model,
                    embedding_model,
                    indexable_document,
                )
                for indexable_document in indexable_documents
            ]

            for document, document_chunk_future in zip(
                indexable_documents, document_chunk_futures
            ):
                document_chunks = document_chunk_future.result()

                document.num_chunks = len(document_chunks)
                document.embedding = np.mean(
                    [document_chunk.embedding for document_chunk in document_chunks],
                    axis=0,
                )
                DocumentChunk.save_bulk(document_chunks)
                document.save()

                progress_bar()


def get_indexable_documents(
    resolved: List[Tuple[str, str]], completion_model: ConfiguredModel
) -> List[Document]:
    """
    Get indexable documents
    """
    document_ids = [
        document_id
        for document_id in [
            get_document_id(doc_path, doc_type) for doc_path, doc_type in resolved
        ]
        if document_id is not None
    ]
    documents = Document.load_bulk(document_ids)
    indexable_documents = []

    for doc, (path, doc_type) in zip(documents, resolved):
        indexable_doc = get_indexable_document(doc, path, doc_type, completion_model)
        if indexable_doc is not None:
            indexable_documents.append(indexable_doc)

    return indexable_documents


def get_indexable_document(
    document: Optional[Document],
    document_path: str,
    document_type: str,
    completion_model: ConfiguredModel,
) -> Optional[Document]:
    """
    Get indexable document
    """
    document_text = read_document(document_path, document_type)
    if not document_text:
        return None

    document_text_bytes = document_text.encode("utf-8")
    doc_hash = hashlib.sha256(document_text_bytes).hexdigest()

    if document and document.id == doc_hash:
        return None

    return Document(
        {
            "id": doc_hash,
            "path": document_path,
            "document_type": document_type,
            "num_chunks": document.num_chunks if document else 0,
            "size": len(document_text_bytes),
            "tokens": get_token_count(completion_model, document_text),
        }
    )


def create_document_chunks(
    completion_model: ConfiguredModel,
    embedding_model: ConfiguredModel,
    indexable_document: Document,
):
    """
    This function is used to create a tree of responses from the OpenAI API
    """
    # key for each chunk embedding is {file_hash}_chunk_id
    # then the key for each file embedding is {file_hash}

    # IMPORTANT NOTE:
    # if we want to be able to track file histories and such, we should have the file hash be determined by git's native hasing
    # run command: git hash-object {file_name}

    # ("{hash}", [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], {"type": "file", "num_chunks": 5, "num_tokens": 100})
    # ("{hash}_{chunk_id}", [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], {"summary": "chunk_summary", "start_pos": "0", "end_pos": "100", "num_tokens": 50})

    text: Optional[str] = read_document(
        indexable_document.path, indexable_document.document_type
    )
    if not text:
        return []

    tokens = get_token_count(completion_model, text)
    if tokens < completion_model.soft_token_limit:
        summary: str = completion_model(
            build_prompt(
                [
                    create_message(Role.SYSTEM.value, INDEX_PROMPT_PREFIX),
                    create_message(Role.USER.value, text),
                ],
                completion_model,
            )
        )
        document_chunk = DocumentChunk(
            {
                "id": f"{indexable_document.id}_0",
                "summary": summary,
                "embedding": embedding_model(summary),
                "start_pos": 0,
                "end_pos": len(text),
                "num_tokens": tokens,
            }
        )
        return [document_chunk]

    document_chunks: List[DocumentChunk] = split_raw_text_to_vectors(
        completion_model, embedding_model, text, indexable_document.id
    )
    document_chunk_tree = create_tree(document_chunks, completion_model)

    return collect_leaves_with_embeddings(document_chunk_tree, "", embedding_model)


def split_raw_text_to_vectors(
    completion_model: ConfiguredModel,
    embedding_model: ConfiguredModel,
    text: str,
    document_hash: str,
) -> List[DocumentChunk]:
    """
    Splits text into smaller chunks to not exceed the token limit.
    """
    start = 0
    end = len(text)
    document_chunks: List[DocumentChunk] = []

    while start < end:
        # Use binary search to find the maximum chunk size in terms of tokens that fits within the token limit
        text_chunk_size = binary_search_max_raw_text_chunk_size(
            completion_model, text, start, end
        )

        # Split the chunk and add it as a new node
        text_str = text[start : start + text_chunk_size]
        summary: str = completion_model(
            build_prompt(
                [
                    create_message(Role.SYSTEM.value, INDEX_PROMPT_PREFIX),
                    create_message(Role.USER.value, text_str),
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
                    "num_tokens": get_token_count(completion_model, text_str),
                }
            )
        )

        # Update start pointer to point to the start of the next chunk
        start += text_chunk_size

    return document_chunks


def binary_search_max_raw_text_chunk_size(
    completion_model: ConfiguredModel, text: str, start: int, end: int
) -> int:
    """
    Uses binary search to find the maximum chunk size in terms of tokens that fits within the token limit.
    """
    left = 0
    right = end - start
    while left < right:
        mid = (left + right + 1) // 2
        if (
            get_token_count(completion_model, text[start : start + mid])
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


def create_tree(nodes: List[T], completion_model: ConfiguredModel) -> Node:
    summary = " ".join(node.summary for node in nodes)
    if get_token_count(completion_model, summary) <= completion_model.soft_token_limit:
        summary = " ".join(node.summary for node in nodes)
        node_id = f"parent_{nodes[0].id.split('_')[0]}"
        return Node(node_id, summary, nodes)

    mid = len(nodes) // 2
    left_tree = create_tree(nodes[:mid], completion_model)
    right_tree = create_tree(nodes[mid:], completion_model)

    merged_summary = completion_model(
        build_prompt(
            [
                create_message(Role.SYSTEM.value, INDEX_PROMPT_PREFIX),
                create_message(
                    Role.USER.value, f"{left_tree.summary} {right_tree.summary}"
                ),
            ],
            completion_model,
        )
    )

    parent_id = f"parent_{left_tree.id.split('_')[1]}_{right_tree.id.split('_')[1]}"
    parent_node = Node(parent_id, merged_summary, [left_tree, right_tree])

    return parent_node


def collect_leaves_with_embeddings(
    node: T,
    ancestor_summaries: str,
    embedding_model: ConfiguredModel,
) -> List[DocumentChunk]:
    if isinstance(node, DocumentChunk):
        leaf = node
        leaf.embedding = embedding_model(f"{ancestor_summaries} {node.summary}")
        return [leaf]

    leaves = []
    for child in node.children:
        leaves.extend(
            collect_leaves_with_embeddings(
                child, f"{ancestor_summaries} {node.summary}", embedding_model
            )
        )

    return leaves
