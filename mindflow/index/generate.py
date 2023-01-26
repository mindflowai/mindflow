"""
Generate an index for a list of documents.
"""

from asyncio import Future
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

from alive_progress import alive_bar

from mindflow.client.mindflow.get_unindexed_documents import (
    get_unindexed_documents as remote_get_unindexed_documents,
)
from mindflow.client.mindflow.index_documents import (
    index_documents as remote_index_documents,
)
from mindflow.index.model import index, DocumentReference

PACKET_SIZE = 2 * 1024 * 1024


def generate_index(document_references: List[DocumentReference], **kwargs):
    """
    Generate an index for a list of documents.
    """

    packets: List[DocumentReference] = create_packets(document_references)

    # Create a thread pool with 4 worker threads
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit the tasks to the thread pool
        results: List[Future[int]] = [
            executor.submit(create_index, packet, **kwargs) for packet in packets
        ]

        with alive_bar(
            sum(len(packet) for packet in packets), bar="blocks", spinner="twirls"
        ) as progress_bar:
            # Process the results as they complete
            for complete in as_completed(results):
                progress_bar(complete.result())


def create_packets(
    document_references: List[DocumentReference],
) -> List[List[DocumentReference]]:
    """
    Creates small packets of files to process.
    """
    packets: List[List[DocumentReference]] = []
    packet: List[DocumentReference] = []

    packet_size: int = 0
    total_size: int = 0

    for document_reference in document_references:
        if packet_size + document_reference.doc_size <= PACKET_SIZE:
            packet.append(document_reference)
            packet_size += document_reference.doc_size
        else:
            packets.append(packet)
            packet = [document_reference]
            packet_size = document_reference.doc_size
            total_size += packet_size

    if packet:
        packets.append(packet)
        total_size += packet_size

    print(f"Total content size: MB {total_size / 1024 / 1024:.2f}")
    return packets


def create_index(document_references: List[DocumentReference], **kwargs) -> int:
    """
    Create an index for a list of documents.
    """
    if kwargs.get("remote", True):
        documents_references_to_index: List[
            DocumentReference
        ] = remote_get_unindexed_documents(document_references)
        if documents_references_to_index:
            remote_index_documents(documents_references_to_index)
    else:
        index.index_documents(document_references, **kwargs)

    return len(document_references)
