"""
Module containing logic to build search tree for document index.
"""

# from transformers import GPT2TokenizerFast
from typing import List
from collections import deque

from mindflow.client.openai.gpt import GPT
from mindflow.utils.prompts import SEARCH_INDEX
from mindflow.utils.config import config as Config

# import warnings

# warnings.filterwarnings("ignore", category=UserWarning, module='transformers')


class Node:
    """
    Simple node class for search tree.
    """

    def __init__(self, text: str, start: int, end: int, leaves: List["Node"]):
        self.start = start
        self.end = end
        self.summary = GPT.get_completion(
            SEARCH_INDEX, text, Config.GPT_MODEL_COMPLETION
        )
        self.embedding = GPT.get_embedding(text, Config.GPT_MODEL_EMBEDDING)
        self.leaves = leaves


class TextChunk:
    """
    Simple text chunk class for handling text chunks.
    """

    def __init__(self, text: str, start: int, end: int):
        self.start = start
        self.end = end
        self.text = text


def count_tokens(text: str) -> int:
    """
    Counts/estimates the number of tokens this text will consume by GPT.
    """
    # tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    # count = len(tokenizer(text)['input_ids'])
    return len(text) / 4  # Token Estimation for speed


def tree_to_dict(root: Node) -> dict:
    """
    Iteratively convert the Node tree to a dictionary.
    """
    tree_dict = {
        "start": root.start,
        "end": root.end,
        "summary": root.summary,
        "embedding": root.embedding,
        "leaves": [],
    }
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node.leaves:
            for leaf in node.leaves:
                queue.append(leaf)
                tree_dict["leaves"].append(
                    {
                        "start": leaf.start,
                        "end": leaf.end,
                        "summary": leaf.summary,
                        "embedding": root.embedding,
                        "leaves": [],
                    }
                )
    return tree_dict


# This function is used to split a string into chunks of a specified token limit using binary search
def binary_split_raw_text_to_nodes(text: str) -> List[Node]:
    """
    Splits text into smaller chunks to not exceed the token limit.
    """
    nodes = []
    stack = [(text, 0, len(text))]
    while stack:
        text, start, end = stack.pop()
        if count_tokens(text[start:end]) < Config.SEARCH_INDEX_TOKEN_LIMIT:
            nodes.append(
                Node(
                    text[start:end],
                    start + start,
                    start + end,
                    []
                )
            )
        else:
            mid = (start + end) // 2
            stack.append((text, start, mid))
            stack.append((text, mid, end))
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
            < Config.SEARCH_INDEX_TOKEN_LIMIT
        ):
            chunks.append(nodes[start:end])
        else:
            mid = (start + end) // 2
            stack.append((nodes, start, mid))
            stack.append((nodes, mid, end))
    return chunks


def create_nodes(leaf_nodes: List[Node]) -> Node:
    """
    This function is used to iteratively create a nodes of our search tree
    """
    stack = [(leaf_nodes, 0, len(leaf_nodes))]
    while stack:
        leaf_nodes, start, end = stack.pop()
        if (
            sum(count_tokens(leaf_node.summary) for leaf_node in leaf_nodes[start:end])
            > Config.SEARCH_INDEX_TOKEN_LIMIT
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
            return Node(
                parent_node_summaries,
                leaf_nodes[start].start,
                leaf_nodes[end - 1].end,
                leaf_nodes[start:end],
            )


def create_text_search_tree(text: str) -> dict:
    """
    This function is used to create a tree of responses from the OpenAI API
    """
    if count_tokens(text) < Config.SEARCH_INDEX_TOKEN_LIMIT:
        return tree_to_dict(Node(text, 0, len(text), []))

    return tree_to_dict(create_nodes(binary_split_raw_text_to_nodes(text)))
