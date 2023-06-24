import asyncio
import hashlib
import sys

from typing import List, Optional

from alive_progress import alive_bar
import numpy as np
from result import Err, Ok, Result

from mindflow.core.types.document import (
    Document,
    DocumentChunk,
    DocumentReference,
    get_document_id,
)
from mindflow.core.types.model import (
    ConfiguredTextCompletionModel,
    ConfiguredEmbeddingModel,
    ModelApiCallError,
)
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


async def run_index(settings: Settings, document_paths: List[str]) -> str:
    index_model: ConfiguredTextCompletionModel = settings.mindflow_models.index
    embedding_model: ConfiguredEmbeddingModel = settings.mindflow_models.embedding

    document_references: List[DocumentReference] = resolve_paths_to_document_references(
        document_paths
    )

    if not (
        indexable_documents := await get_indexable_documents(
            document_references, index_model
        )
    ):
        return "No documents to index"

    print_total_size_of_documents(indexable_documents)
    print_total_tokens_and_ask_to_continue(indexable_documents, index_model)

    await index_documents(indexable_documents, index_model, embedding_model)

    return "Indexing complete"


async def get_indexable_documents(
    document_references: List[DocumentReference],
    index_model: ConfiguredTextCompletionModel,
) -> List[Document]:
    document_ids = [
        document_id
        for document_id in [
            get_document_id(document_reference.path, document_reference.document_type)
            for document_reference in document_references
        ]
        if document_id is not None
    ]
    documents: List[Optional[Document]] = await Document.load_bulk(document_ids)
    return [
        indexable_document
        for document, document_reference in zip(documents, document_references)
        if (
            indexable_document := get_indexable_document(
                document, document_reference, index_model
            )
        )
        is not None
    ]


def get_indexable_document(
    document: Optional[Document],
    document_reference: DocumentReference,
    index_model: ConfiguredTextCompletionModel,
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
                index_model.tokenizer, document_text
            ),
        }
    )


def print_total_size_of_documents(documents: List[Document]):
    print(
        f"Total content size: MB {sum([document.size for document in documents]) / 1024 / 1024:.2f}"
    )


def print_total_tokens_and_ask_to_continue(
    documents: List[Document],
    index_model: ConfiguredTextCompletionModel,
    usd_threshold: float = 0.5,
):
    total_tokens = sum([document.tokens for document in documents])
    print(f"Total tokens: {total_tokens}")
    total_cost_usd: float = (
        total_tokens / float(index_model.model.token_cost_unit)
    ) * index_model.model.token_cost
    if total_cost_usd > usd_threshold:
        print(f"Total cost: ${total_cost_usd:.2f}")
        while True:
            if (
                user_input := input("Would you like to continue? (yes/no): ").lower()
            ) in ["no", "n"]:
                sys.exit(0)
            elif user_input in ["yes", "y"]:
                break
            print("Invalid input. Please try again.")


async def index_documents(
    documents: List[Document],
    index_model: ConfiguredTextCompletionModel,
    embedding_model: ConfiguredEmbeddingModel,
) -> None:
    print("Starting to index documents...")
    with alive_bar(len(documents), bar="blocks", spinner="twirls") as progress_bar:
        tasks = [
            index_document(indexable_document, index_model, embedding_model)
            for indexable_document in documents
        ]

        for future in asyncio.as_completed(tasks):
            index_document_result = await future
            if isinstance(index_document_result, Err):
                print(f"Failed to index document {index_document_result.value}")
            progress_bar()


async def index_document(
    indexable_document: Document,
    index_model: ConfiguredTextCompletionModel,
    embedding_model: ConfiguredEmbeddingModel,
) -> Result[bool, ModelApiCallError]:
    if not (
        text := read_document(indexable_document.path, indexable_document.document_type)
    ):
        print("Document staged for indexing could not be read")
        sys.exit(1)

    partitioned_nodes_result: Result[
        List[Node], ModelApiCallError
    ] = await partition_document_into_nodes(text, index_model)
    if isinstance(partitioned_nodes_result, Err):
        return partitioned_nodes_result

    hierarchical_summary_tree_result: Result[
        Node, ModelApiCallError
    ] = await create_hierarchical_summary_tree(
        partitioned_nodes_result.value,
        index_model,
    )
    if isinstance(hierarchical_summary_tree_result, Err):
        return hierarchical_summary_tree_result

    document_chunks_result: Result[
        List[DocumentChunk], ModelApiCallError
    ] = await collect_leaves_with_embeddings_from_appended_branch_summaries(
        indexable_document.id,
        hierarchical_summary_tree_result.value,
        embedding_model,
    )

    if isinstance(document_chunks_result, Err):
        return document_chunks_result

    indexable_document.num_chunks = len(document_chunks_result.value)
    indexable_document.embedding = list(
        np.mean(
            [
                document_chunk.embedding
                for document_chunk in document_chunks_result.value
            ],
            axis=0,
        )
    )

    await asyncio.gather(
        *[
            DocumentChunk.save_bulk(document_chunks_result.value),
            indexable_document.save(),
        ]
    )
    return Ok(True)


class Node:
    def __init__(
        self, start_pos: int, end_pos: int, summary: str, children: List["Node"]
    ):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.summary = summary
        self.children = children

    @classmethod
    async def create_node(
        cls,
        text: str,
        start_pos: int,
        end_pos: int,
        index_model: ConfiguredTextCompletionModel,
        children: List["Node"] = [],
    ) -> Result["Node", ModelApiCallError]:
        prompt = build_prompt_from_conversation_messages(
            [
                create_conversation_message(Role.SYSTEM.value, INDEX_PROMPT_PREFIX),
                create_conversation_message(Role.USER.value, f"{text}..."),
            ],
            index_model,
        )

        index_model_result = await index_model.call_api(prompt)
        if isinstance(index_model_result, Err):
            return index_model_result

        return Ok(cls(start_pos, end_pos, index_model_result.value, children))

    def __repr__(self):
        return f"Node(start_pos={self.start_pos}, end_pos={self.end_pos}, summary={self.summary}, children={self.children})"


async def partition_document_into_nodes(
    text: str,
    index_model: ConfiguredTextCompletionModel,
) -> Result[List[Node], ModelApiCallError]:
    start = 0
    end = len(text)
    document_partition_nodes: List[Node] = []
    tasks: List[asyncio.Task[Result[Node, ModelApiCallError]]] = []

    while start < end:
        text_chunk_size = binary_search_max_raw_text_chunk_size_for_token_limit(
            text, start, end, index_model
        )
        tasks.append(
            asyncio.create_task(
                Node.create_node(
                    text[start : start + text_chunk_size],
                    start,
                    start + text_chunk_size,
                    index_model,
                )
            )
        )
        start += text_chunk_size

    for future in asyncio.as_completed(tasks):
        if isinstance(node_result := await future, Err):
            return node_result
        document_partition_nodes.append(node_result.value)

    return Ok(document_partition_nodes)


def binary_search_max_raw_text_chunk_size_for_token_limit(
    text: str, start: int, end: int, index_model: ConfiguredTextCompletionModel
) -> int:
    left = 0
    right = end - start
    while left < right:
        mid = (left + right + 1) // 2
        if (
            get_token_count_of_text_for_model(
                index_model.tokenizer, text[start : start + mid]
            )
            <= index_model.config.soft_token_limit
        ):
            left = mid
            continue
        right = mid - 1
    return left


async def create_hierarchical_summary_tree(
    nodes: List[Node], index_model: ConfiguredTextCompletionModel
) -> Result[Node, ModelApiCallError]:
    if len(nodes) == 1:
        return Ok(nodes[0])

    if (
        get_token_count_of_text_for_model(
            index_model.tokenizer,
            (appended_summaries := " ".join(node.summary for node in nodes)),
        )
        <= index_model.config.soft_token_limit
    ):
        return await Node.create_node(
            appended_summaries,
            nodes[0].start_pos,
            nodes[-1].end_pos,
            index_model,
            nodes,
        )

    mid = len(nodes) // 2
    tasks: List[asyncio.Task[Result[Node, ModelApiCallError]]] = [
        asyncio.create_task(create_hierarchical_summary_tree(nodes[:mid], index_model)),
        asyncio.create_task(create_hierarchical_summary_tree(nodes[mid:], index_model)),
    ]

    tree_result: List[Result[Node, ModelApiCallError]] = await asyncio.gather(*tasks)
    if isinstance(tree_result[0], Err):
        return tree_result[0]
    if isinstance(tree_result[1], Err):
        return tree_result[1]

    left_tree, right_tree = tree_result[0].value, tree_result[1].value
    return await Node.create_node(
        f"{left_tree.summary} {right_tree.summary}",
        left_tree.start_pos,
        right_tree.end_pos,
        index_model,
        [left_tree, right_tree],
    )


async def create_document_chunk(
    id: str,
    start_pos: int,
    end_pos: int,
    appended_summaries: str,
    embedding_model: ConfiguredEmbeddingModel,
) -> Result[DocumentChunk, ModelApiCallError]:
    embedding_result = await embedding_model.call_api(appended_summaries)
    if isinstance(embedding_result, Err):
        return embedding_result

    return Ok(
        DocumentChunk(
            {
                "id": id,
                "start_pos": start_pos,
                "end_pos": end_pos,
                "summary": appended_summaries,
                "embedding": list(embedding_result.value),
            }
        )
    )


async def collect_leaves_with_embeddings_from_appended_branch_summaries(
    document_hash: str,
    root_node: Node,
    embedding_model: ConfiguredEmbeddingModel,
) -> Result[List[DocumentChunk], ModelApiCallError]:
    stack = [(root_node, "")]
    tasks: List[asyncio.Task[Result[DocumentChunk, ModelApiCallError]]] = []
    document_chunk_id = 0
    while stack:
        node, ancestor_summaries = stack.pop()
        if not node.children:
            tasks.append(
                asyncio.create_task(
                    create_document_chunk(
                        f"{document_hash}_{document_chunk_id}",
                        node.start_pos,
                        node.end_pos,
                        f"{ancestor_summaries} {node.summary}",
                        embedding_model,
                    )
                )
            )
            document_chunk_id += 1
        else:
            for child in node.children:
                stack.append((child, f"{ancestor_summaries} {node.summary}"))

    create_document_chunk_result: List[
        Result[DocumentChunk, ModelApiCallError]
    ] = await asyncio.gather(*tasks)

    for result in create_document_chunk_result:
        if isinstance(result, Err):
            return result

    return Ok(
        [
            result.value
            for result in create_document_chunk_result
            if isinstance(result, Ok)
        ]
    )
