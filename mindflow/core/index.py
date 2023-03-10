"""
`generate` command
"""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy

from typing import Dict, List, Union
from typing import Optional

import numpy as np
from alive_progress import alive_bar  # type: ignore

from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.objects.document import Document
from mindflow.db.objects.document import DocumentReference
from mindflow.db.objects.document import read_document
from mindflow.db.objects.model import ConfiguredModel
from mindflow.resolving.resolve import resolve_all
from mindflow.settings import Settings
from mindflow.utils.errors import ModelError
from mindflow.utils.helpers import (
    print_total_size,
    print_total_tokens_and_ask_to_continue,
)
from mindflow.utils.prompt_builders import build_context_prompt
from mindflow.utils.prompts import INDEX_PROMPT_PREFIX
from mindflow.utils.token import get_batch_token_count, get_token_count


def run_index(document_paths: List[str], refresh: bool, verbose: bool = True) -> None:
    """
    This function is used to generate an index and/or embeddings for files
    """

    import os

    document_paths = [os.path.abspath(path) for path in document_paths]

    settings = Settings()
    completion_model: ConfiguredModel = settings.mindflow_models.index.model

    ## Resolve documents to document references
    resolved: List[Dict] = resolve_all(document_paths)
    document_references: List[DocumentReference] = DocumentReference.from_resolved(
        resolved, completion_model
    )

    ## Filter out documents that are already indexed
    indexable_document_references: List[DocumentReference] = return_if_indexable(
        document_references, refresh
    )
    if not indexable_document_references:
        if verbose:
            print("No documents to index")
        return

    print_total_size(indexable_document_references)
    print_total_tokens_and_ask_to_continue(
        indexable_document_references, completion_model
    )

    # build search trees in parallel
    with alive_bar(
        len(indexable_document_references), bar="blocks", spinner="twirls"
    ) as progress_bar:
        with ThreadPoolExecutor(max_workers=50) as executor:
            search_tree_futures = [
                executor.submit(
                    create_text_search_tree,
                    completion_model,
                    read_document(
                        document_reference.path, document_reference.document_type
                    ),  # type: ignore
                )
                for document_reference in indexable_document_references
            ]

            for search_tree_future, document_reference in zip(
                search_tree_futures, indexable_document_references
            ):
                document: Document = document_reference.to_document()
                document.search_tree = search_tree_future.result()
                document.save()
                del document_reference, search_tree_future
                progress_bar()

    DATABASE_CONTROLLER.databases.json.save_file()


def return_if_indexable(
    document_references: List[DocumentReference], refresh: bool
) -> List[DocumentReference]:
    return [
        document_reference
        for document_reference in document_references
        if index_document(document_reference, refresh)
    ]


def index_document(document_reference: DocumentReference, refresh: bool) -> bool:
    if not hasattr(document_reference, "hash") or not document_reference.hash:
        return True
    if refresh:
        return True
    return document_reference.hash != document_reference.new_hash


class Node:
    """
    Simple node class for search tree.
    """

    start: int
    end: int
    summary: str
    embedding: np.ndarray
    leaves: List["Node"]

    def __init__(
        self,
        completion_model: ConfiguredModel,
        start: int,
        end: int,
        text: Optional[str] = None,
    ):
        self.start = start
        self.end = end
        if text:
            response: Union[str, ModelError] = completion_model(
                build_context_prompt(INDEX_PROMPT_PREFIX, text)
            )
            if isinstance(response, ModelError):
                self.summary = ""
                print(response.index_message)
            else:
                self.summary = response

    def set_leaves(self, leaves: List["Node"]) -> None:
        self.leaves = leaves

    def to_dict(self) -> dict:
        return {
            "start": self.start,
            "end": self.end,
            "summary": self.summary if hasattr(self, "summary") else None,
            "embedding": self.embedding if hasattr(self, "embedding") else None,
            "leaves": [leaf.to_dict() for leaf in self.leaves]
            if hasattr(self, "leaves")
            else None,
        }

    def iterative_to_dict(self) -> dict:
        # Can't figure out what is wrong with this yet. Leaves coming up null.
        stack = [(self, None)]
        while stack:
            node, parent_leaves = stack.pop()
            node_dict: dict = {
                "start": node.start,
                "end": node.end,
                "summary": node.summary if hasattr(node, "summary") else None,
                "embedding": node.embedding if hasattr(node, "embedding") else None,
                "leaves": [],
            }
            if parent_leaves:
                parent_leaves.append(node_dict)
            if hasattr(node, "leaves"):
                for leaf in node.leaves:
                    leaves = node_dict["leaves"]
                    stack.append((leaf, leaves))
        return node_dict


# This function is used to split a string into chunks of a specified token limit using binary search
def binary_split_raw_text_to_nodes(
    completion_model: ConfiguredModel, text: str
) -> List[Node]:
    """
    Splits text into smaller chunks to not exceed the token limit.
    """
    nodes = []
    stack = [(0, len(text))]
    while stack:
        start, end = stack.pop()
        if (
            get_token_count(completion_model, text[start:end])
            < completion_model.soft_token_limit
        ):
            nodes.append(Node(completion_model, start, end, text[start:end]))
        else:
            mid = ((end - start) // 2) + start
            stack.append((start, mid))
            stack.append((mid, end))
    return nodes


def binary_split_nodes_to_chunks(
    completion_model: ConfiguredModel, nodes: List[Node]
) -> List[List[Node]]:
    """
    Split nodes into smaller chunks to not exceed the token limit.
    """
    chunks = []
    stack = [(nodes, 0, len(nodes))]
    while stack:
        nodes, start, end = stack.pop()
        if (
            get_batch_token_count(
                completion_model, [node.summary for node in nodes[start:end]]
            )
            < completion_model.soft_token_limit
        ):
            chunks.append(nodes[start:end])
        else:
            mid = (start + end) // 2
            stack.append((nodes, deepcopy(start), mid))
            stack.append((nodes, mid, deepcopy(end)))
    return chunks


def create_nodes(completion_model: ConfiguredModel, leaf_nodes: List[Node]) -> Node:
    """
    This function is used to iteratively create a nodes of our search tree
    """
    stack = [(leaf_nodes, 0, len(leaf_nodes))]
    while stack:
        leaf_nodes, start, end = stack.pop()
        if (
            get_batch_token_count(
                completion_model,
                [leaf_node.summary for leaf_node in leaf_nodes[start:end]],
            )
            > completion_model.soft_token_limit
        ):
            node_chunks: List[List[Node]] = binary_split_nodes_to_chunks(
                completion_model, leaf_nodes[start:end]
            )
            for node_chunk in node_chunks:
                stack.append((node_chunk, 0, len(node_chunk)))
        else:
            parent_node_summaries = "\n".join(
                [node.summary for node in leaf_nodes[start:end]]
            )
            node = Node(
                completion_model,
                leaf_nodes[start].start,
                leaf_nodes[end - 1].end,
                parent_node_summaries,
            )
            node.set_leaves(leaf_nodes[start:end])
            return node
    return Node(completion_model, 0, 0)


def create_text_search_tree(completion_model: ConfiguredModel, text: str) -> dict:
    """
    This function is used to create a tree of responses from the OpenAI API
    """
    if get_token_count(completion_model, text) < completion_model.soft_token_limit:
        return Node(completion_model, 0, len(text), text).to_dict()

    return create_nodes(
        completion_model, binary_split_raw_text_to_nodes(completion_model, text)
    ).to_dict()
