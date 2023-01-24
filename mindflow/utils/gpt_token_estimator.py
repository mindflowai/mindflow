from transformers import GPT2TokenizerFast
from typing import List

from mindflow.client.openai.gpt import GPT
from mindflow.utils.config import config as Config

SUMMARY_TOKEN_LIMIT = 2000

def count_tokens(input: str):
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    return len(tokenizer(input)['input_ids'])

class Node:
    def __init__(self, text: str, start: int, end: int, leaves: List["Node"] = []):
        self.start = start
        self.end = end
        self.summary = GPT.get_completion(text, Config.GPT_MODEL_COMPLETION)
        self.embedding = GPT.get_embedding(text, Config.GPT_MODEL_EMBEDDING)
        self.leaves = leaves

class TextChunk: 
    def __init__(self, text: str, start: int, end: int):
        self.start = start
        self.end = end
        self.text = text

def tree_to_dict(root: Node) -> dict:
    tree_dict = {
        "start": root.start,
        "end": root.end,
        "summary": root.summary,
        "embedding": root.embedding,
        "leaves": []
    }
    for leaf in root.leaves:
        tree_dict["leaves"].append(tree_to_dict(leaf))
    return tree_dict

# This function is used to split a string into chunks of a specified token limit using binary search
def binary_split_text_into_chunks(text_chunk: TextChunk) -> List[TextChunk]:
    """
    This function is used to split a string into chunks of a specified token limit using binary search
    """
    if count_tokens(text_chunk.text) < SUMMARY_TOKEN_LIMIT:
        return [text_chunk]
    else:
        mid = len(text_chunk.text) // 2
        left_chunks = binary_split_text_into_chunks(TextChunk(text_chunk.text[:mid], text_chunk.start, text_chunk.start + mid))
        right_chunks = binary_split_text_into_chunks(TextChunk(text_chunk.text[mid:], text_chunk.start + mid, text_chunk.end))
        return left_chunks + right_chunks

def binary_split_nodes_into_chunks(nodes: List[Node]) -> List[List[Node]]:
    """
    This function is used to split a list of nodes into chunks of a specified token limit using binary search
    """
    if (count_tokens(node.text) for node in nodes) < SUMMARY_TOKEN_LIMIT:
        return [nodes]
    else:
        mid = len(nodes) // 2
        left_chunks = binary_split_nodes_into_chunks(nodes[:mid])
        right_chunks = binary_split_nodes_into_chunks(nodes[mid:])
        return left_chunks + right_chunks


def recurse_nodes(leaf_nodes: List[Node]) -> Node:
    """
    This function is used to recursively create a tree of responses from the OpenAI API
    """
    parent_nodes: Node = []
    if (count_tokens(summary) for summary in leaf_nodes) > SUMMARY_TOKEN_LIMIT:
        node_chunks: List[List[Node]] = binary_split_nodes_into_chunks(leaf_nodes)
        for node_chunk in node_chunks:
            parent_nodes.append(recurse_nodes(node_chunk))
    else:
        parent_nodes = leaf_nodes
    
    # Append parent node vals together
    parent_node_vals = "\n".join([node.val for node in parent_nodes])
    return Node(parent_node_vals, parent_nodes[0].start, parent_nodes[-1].end, parent_nodes)

def create_text_search_tree(text: str) -> dict:
    """
    This function is used to create a tree of responses from the OpenAI API
    """
    if count_tokens(text) < SUMMARY_TOKEN_LIMIT:
        return tree_to_dict(Node(text, 0, len(text)))
    else:
        text_chunks = binary_split_text_into_chunks(text)
        text_summary_nodes = [Node(text_chunk.text, text_chunk.start, text_chunk.end) for text_chunk in text_chunks]
        tree_to_dict(recurse_nodes(text_summary_nodes))