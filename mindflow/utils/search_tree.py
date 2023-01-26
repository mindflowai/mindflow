"""
Module containing logic to build search tree for document index.
"""

# from transformers import GPT2TokenizerFast
from typing import List
from copy import deepcopy

import numpy as np


from mindflow.client.openai.gpt import GPT
from mindflow.utils.prompts import SEARCH_INDEX
from mindflow.utils.config import config as CONFIG
from mindflow.utils.helpers import IndexType

# import warnings
# warnings.filterwarnings("ignore", category=UserWarning, module='transformers')


class Node:
    """
    Simple node class for search tree.
    """

    start: int
    end: int
    summary: str
    embedding: np.ndarray
    leaves: List["Node"]

    def __init__(self, index_type: str, start: int, end: int, text: str = None):
        self.start = start
        self.end = end
        if text:
            if index_type == IndexType.DEEP:
                self.summary = GPT.get_completion(
                    SEARCH_INDEX, text, CONFIG.GPT_MODEL_COMPLETION
                )
            else:
                self.embedding = GPT.get_embedding(text, CONFIG.GPT_MODEL_EMBEDDING)

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
            node_dict = {
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
    return len(text) / 4  # Token Estimation for speed


# This function is used to split a string into chunks of a specified token limit using binary search
def binary_split_raw_text_to_nodes(text: str, index_type: str) -> List[Node]:
    """
    Splits text into smaller chunks to not exceed the token limit.
    """
    nodes = []
    stack = [(0, len(text))]
    while stack:
        start, end = stack.pop()
        if count_tokens(text[start:end]) < CONFIG.SEARCH_INDEX_TOKEN_LIMIT:
            nodes.append(Node(index_type, start, end, text[start:end]))
        else:
            mid = ((end - start) // 2) + start
            stack.append((start, mid))
            stack.append((mid, end))
    return nodes


def binary_split_nodes_to_chunks(nodes: List[Node]) -> List[List[Node]]:
    """
    Split nodes into smaller chunks to not exceed the token limit.
    """
    chunks = []
    stack = [(nodes, 0, len(nodes))]
    while stack:
        nodes, start, end = stack.pop()
        if (
            sum(count_tokens(node.summary) for node in nodes[start:end])
            < CONFIG.SEARCH_INDEX_TOKEN_LIMIT
        ):
            chunks.append(nodes[start:end])
        else:
            mid = (start + end) // 2
            stack.append((nodes, deepcopy(start), mid))
            stack.append((nodes, mid, deepcopy(end)))
    return chunks


def create_nodes(leaf_nodes: List[Node], index_type: str) -> Node:
    """
    This function is used to iteratively create a nodes of our search tree
    """
    if index_type == IndexType.SHALLOW:
        print(f"start: {leaf_nodes[0].start}, end: {leaf_nodes[-1].end}")
        return Node(index_type, leaf_nodes[0].start, leaf_nodes[-1].end)

    stack = [(leaf_nodes, 0, len(leaf_nodes))]
    while stack:
        leaf_nodes, start, end = stack.pop()
        if (
            sum(count_tokens(leaf_node.summary) for leaf_node in leaf_nodes[start:end])
            > CONFIG.SEARCH_INDEX_TOKEN_LIMIT
        ):
            node_chunks: List[List[Node]] = binary_split_nodes_to_chunks(
                leaf_nodes[start:end]
            )
            for node_chunk in node_chunks:
                stack.append((node_chunk, 0, len(node_chunk)))
        else:
            parent_node_summaries = "\n".join(
                [node.summary for node in leaf_nodes[start:end]]
            )
            node = Node(
                index_type,
                leaf_nodes[start].start,
                leaf_nodes[end - 1].end,
                parent_node_summaries,
            )
            node.set_leaves(leaf_nodes[start:end])
            return node


def create_text_search_tree(text: str, index_type: bool) -> dict:
    """
    This function is used to create a tree of responses from the OpenAI API
    """
    if count_tokens(text) < CONFIG.SEARCH_INDEX_TOKEN_LIMIT:
        return Node(index_type, 0, len(text), text).to_dict()
    raw_text_nodes = binary_split_raw_text_to_nodes(text, index_type)
    if index_type == IndexType.SHALLOW:
        shallow_search_tree = Node(index_type, 0, len(text))
        shallow_search_tree.set_leaves(raw_text_nodes)
        return shallow_search_tree.to_dict()
    return create_nodes(
        binary_split_raw_text_to_nodes(text, index_type), index_type
    ).to_dict()
