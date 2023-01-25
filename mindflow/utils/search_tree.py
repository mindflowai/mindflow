#from transformers import GPT2TokenizerFast
from collections import deque
from typing import List

from mindflow.client.openai.gpt import GPT
from mindflow.utils.config import config as Config
from mindflow.utils.prompts import SEARCH_INDEX
from mindflow.utils.config import config as Config
# import warnings

# warnings.filterwarnings("ignore", category=UserWarning, module='transformers')

class Node:
    def __init__(self, text: str, start: int, end: int, leaves: List["Node"] = []):
        self.start = start
        self.end = end
        self.summary = GPT.get_completion(SEARCH_INDEX, text, Config.GPT_MODEL_COMPLETION)
        self.embedding = GPT.get_embedding(text, Config.GPT_MODEL_EMBEDDING)
        self.leaves = leaves

class TextChunk: 
    def __init__(self, text: str, start: int, end: int):
        self.start = start
        self.end = end
        self.text = text

def count_tokens(input: str) -> int:
    #tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    #count = len(tokenizer(input)['input_ids'])
    return len(input) / 4 # Token Estimation for speed

def iterative_tree_to_dict(root: Node) -> dict:
    tree_dict = {
        "start": root.start,
        "end": root.end,
        "summary": root.summary,
        "embedding": root.embedding,
        "leaves": []
    }
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node.leaves:
            for leaf in node.leaves:
                queue.append(leaf)
                tree_dict["leaves"].append({
                    "start": leaf.start,
                    "end": leaf.end,
                    "summary": leaf.summary,
                    "embedding": root.embedding,
                    "leaves": []
                })
    return tree_dict

# This function is used to split a string into chunks of a specified token limit using binary search
def iterative_binary_split_text_into_chunks(text_chunk: TextChunk) -> List[TextChunk]:
    chunks = []
    stack = [(text_chunk, 0, len(text_chunk.text))]
    while stack:
        text_chunk, start, end = stack.pop()
        if count_tokens(text_chunk.text[start:end]) < Config.SEARCH_INDEX_TOKEN_LIMIT:
            chunks.append(TextChunk(text_chunk.text[start:end], text_chunk.start + start, text_chunk.start + end))
        else:
            mid = (start + end) // 2
            stack.append((text_chunk, start, mid))
            stack.append((text_chunk, mid, end))
    return chunks

def iterative_binary_split_nodes_into_chunks(nodes: List[Node]) -> List[List[Node]]:
    chunks = []
    stack = [(nodes, 0, len(nodes))]
    while stack:
        nodes, start, end = stack.pop()
        if sum([count_tokens(node.summary) for node in nodes[start:end]]) < Config.SEARCH_INDEX_TOKEN_LIMIT:
            chunks.append(nodes[start:end])
        else:
            mid = (start + end) // 2
            stack.append((nodes, start, mid))
            stack.append((nodes, mid, end))
    return chunks


def iterative_create_nodes(leaf_nodes: List[Node]) -> Node:
    """
    This function is used to iteratively create a tree of responses from the OpenAI API
    """
    stack = [(leaf_nodes, 0, len(leaf_nodes))]
    while stack:
        leaf_nodes, start, end = stack.pop()
        if sum([count_tokens(leaf_node.summary) for leaf_node in leaf_nodes[start:end]]) > Config.SEARCH_INDEX_TOKEN_LIMIT:
            node_chunks: List[List[Node]] = iterative_binary_split_nodes_into_chunks(leaf_nodes[start:end])
            for node_chunk in node_chunks:
                stack.append((node_chunk, 0, len(node_chunk)))
        else:
            parent_node_summaries = "\n".join([node.summary for node in leaf_nodes[start:end]])
            return Node(parent_node_summaries, leaf_nodes[start].start, leaf_nodes[end-1].end, leaf_nodes[start:end])

def create_text_search_tree(text: str) -> dict:
    """
    This function is used to create a tree of responses from the OpenAI API
    """
    if count_tokens(text) < Config.SEARCH_INDEX_TOKEN_LIMIT:
        return iterative_tree_to_dict(Node(text, 0, len(text)))
    else:
        text_chunks = iterative_binary_split_text_into_chunks(TextChunk(text,0, len(text)))
        text_summary_nodes = [Node(text_chunk.text, text_chunk.start, text_chunk.end) for text_chunk in text_chunks]
        done = iterative_tree_to_dict(iterative_create_nodes(text_summary_nodes))
        return done
