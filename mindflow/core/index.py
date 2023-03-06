"""
`generate` command
"""
from asyncio import Future
from copy import deepcopy

from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor
import numpy as np

from alive_progress import alive_bar
from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.objects.model import Model

from mindflow.resolving.resolve import return_if_indexable, resolve_all


from mindflow.db.objects.document import Document, DocumentReference
from mindflow.settings import Settings
from mindflow.db.objects.document import read_document

from mindflow.utils.prompt_builders import build_context_prompt

from mindflow.utils.prompts import INDEX_PROMPT_PREFIX

def run_index(document_paths: List[str], refresh: bool, force: bool) -> None:
    """
    This function is used to generate an index and/or embeddings for files
    """

    import os
    document_paths = [os.path.abspath(path) for path in document_paths]

    settings = Settings()
    completion_model: Model = settings.mindflow_models.index.model
    
    indexable_document_references: List[DocumentReference] = return_if_indexable(resolve_all(document_paths), refresh, force)
    if not indexable_document_references:
        print("No documents to index")
        return

    total_size = sum(
        [
            document_reference.size
            for document_reference in indexable_document_references
        ]
    )
    print(f"Total content size: MB {total_size / 1024 / 1024:.2f}")
    # build search trees in parallel
    with alive_bar(
        len(indexable_document_references), bar="blocks", spinner="twirls"
    ) as progress_bar:

        with ThreadPoolExecutor(max_workers=50) as executor:
            search_tree_futures: List[Future[dict]] = [
                executor.submit(
                    create_text_search_tree,
                    completion_model,
                    read_document(
                        document_reference.path, document_reference.document_type
                    ),
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

class Node:
    """
    Simple node class for search tree.
    """

    start: int
    end: int
    summary: str
    embedding: np.ndarray
    leaves: List["Node"]

    def __init__(self, completion_model: Model, start: int, end: int, text: Optional[str] = None):
        self.start = start
        self.end = end
        if text:
            self.summary = completion_model(build_context_prompt(INDEX_PROMPT_PREFIX, text))

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


def count_tokens(text: str) -> int:
    """
    Counts/estimates the number of tokens this text will consume by GPT.
    """
    # tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    # count = len(tokenizer(text)['input_ids'])
    return len(text) // 4  # Token Estimation for speed


# This function is used to split a string into chunks of a specified token limit using binary search
def binary_split_raw_text_to_nodes(completion_model: Model, text: str) -> List[Node]:
    """
    Splits text into smaller chunks to not exceed the token limit.
    """
    nodes = []
    stack = [(0, len(text))]
    while stack:
        start, end = stack.pop()
        if count_tokens(text[start:end]) < completion_model.soft_token_limit:
            nodes.append(Node(completion_model, start, end, text[start:end]))
        else:
            mid = ((end - start) // 2) + start
            stack.append((start, mid))
            stack.append((mid, end))
    return nodes


def binary_split_nodes_to_chunks(completion_model: Model, nodes: List[Node]) -> List[List[Node]]:
    """
    Split nodes into smaller chunks to not exceed the token limit.
    """
    chunks = []
    stack = [(nodes, 0, len(nodes))]
    while stack:
        nodes, start, end = stack.pop()
        if (
            sum(count_tokens(node.summary) for node in nodes[start:end])
            < completion_model.soft_token_limit
        ):
            chunks.append(nodes[start:end])
        else:
            mid = (start + end) // 2
            stack.append((nodes, deepcopy(start), mid))
            stack.append((nodes, mid, deepcopy(end)))
    return chunks


def create_nodes(completion_model: Model, leaf_nodes: List[Node]) -> Node:
    """
    This function is used to iteratively create a nodes of our search tree
    """
    stack = [(leaf_nodes, 0, len(leaf_nodes))]
    while stack:
        leaf_nodes, start, end = stack.pop()
        if (
            sum(count_tokens(leaf_node.summary) for leaf_node in leaf_nodes[start:end])
            > completion_model.soft_token_limit
        ):
            node_chunks: List[List[Node]] = binary_split_nodes_to_chunks(
                completion_model,
                leaf_nodes[start:end]
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


def create_text_search_tree(completion_model: Model, text: str) -> dict:
    """
    This function is used to create a tree of responses from the OpenAI API
    """
    if count_tokens(text) < completion_model.soft_token_limit:
        return Node(completion_model, 0, len(text), text).to_dict()

    return create_nodes(completion_model, binary_split_raw_text_to_nodes(completion_model, text)).to_dict()
