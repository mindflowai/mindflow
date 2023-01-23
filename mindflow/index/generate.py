"""
Generate an index for a list of documents.
"""

from asyncio import Future
from typing import List, Set
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

from alive_progress import alive_bar

from mindflow.client.mindflow.get_unindexed_documents import (
    get_unindexed_documents as remote_get_unindexed_documents,
)
from mindflow.client.mindflow.index_documents import (
    index_documents as remote_index_documents,
)
from mindflow.index.model import Index, index

PACKET_SIZE = 2 * 1024 * 1024


def generate_index(all_documents: List[Index.Document], remote: bool = False):
    """
    Generate an index for a list of documents.
    """

    packets: List[Index.Document] = create_packets(all_documents)

    # Create a thread pool with 4 worker threads
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit the tasks to the thread pool
        results: List[Future[List[Index.Document]]] = [
            executor.submit(create_index, packet, remote) for packet in packets
        ]

        with alive_bar(
            sum(len(packet) for packet in packets), bar="blocks", spinner="twirls"
        ) as progress_bar:
            # Process the results as they complete
            for complete in as_completed(results):
                progress_bar(complete.result())


def create_packets(all_documents: List[Index.Document]) -> List[List[Index.Document]]:
    """
    Creates small packets of files to process.
    """
    with ProcessPoolExecutor(max_workers=4) as executor:
        sizes = list(executor.map(get_size, all_documents))

    packets: List[List[Index.Document]] = []
    packet: List[Index.Document] = []

    packet_size: int = 0
    total_size: int = 0

    for document, size in zip(all_documents, sizes):
        if packet_size + size <= PACKET_SIZE:
            packet.append(document)
            packet_size += size
        else:
            packets.append(packet)
            packet = [document]
            packet_size = size
            total_size += packet_size

    if packet:
        packets.append(packet)
        total_size += packet_size

    print(f"Total content size: MB {total_size / 1024 / 1024:.2f}")
    return packets


def get_size(document: Index.Document) -> int:
    """
    Get the size of a file.
    """
    return document.size


def create_remote_index(documents: List[Index.Document]):
    """
    Create an index for a list of documents.
    """
    documents_to_index: List[Index.Document] = remote_get_unindexed_documents(documents)
    if documents_to_index:
        remote_index_documents(documents_to_index)


def create_local_index(documents: List[Index.Document]):
    """
    Create an index for a list of documents.
    """
    documents_to_index: List[Index.Document] = index.get_unindexed_documents(documents)
    if documents_to_index:
        index.index_documents(documents_to_index)


def create_index(documents: List[Index.Document], remote: bool) -> int:
    """
    Create an index for a list of documents.
    """
    if remote:
        create_remote_index(documents)
    else:
        create_local_index(documents)

    return len(documents)
