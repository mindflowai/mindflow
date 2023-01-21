"""
Generate an index for a list of resolved paths.
"""

from asyncio import Future
from typing import List, Set
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

from alive_progress import alive_bar

from mindflow.clients.mindflow.get_unindexed_references import (
    get_unindexed_references as remote_get_unindexed_references,
)
from mindflow.clients.mindflow.index_references import (
    index_references as remote_index_references,
)
from mindflow.index.resolvers.base_resolver import Resolved
from mindflow.utils.reference import Reference
from mindflow.index.model import index as Index

PACKET_SIZE = 2 * 1024 * 1024


def generate_index(all_resolved: List[Resolved], remote: bool = False):
    """
    Generate an index for a list of resolved paths.
    """

    packets: List[Resolved] = create_packets(all_resolved)

    # Create a thread pool with 4 worker threads
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit the tasks to the thread pool
        results: List[Future[List[Reference]]] = [
            executor.submit(process_packet, packet) for packet in packets
        ]

        with alive_bar(
            sum(len(packet) for packet in packets), bar="blocks", spinner="twirls"
        ) as progress_bar:
            # Process the results as they complete
            for complete in as_completed(results):
                references: List[Reference] = complete.result()
                hashes: List[str] = [reference.hash for reference in references]

                if remote:
                    create_remote_index(references, hashes)
                else:
                    create_local_index(references, hashes)

                progress_bar(len(references))


def create_packets(all_resolved: List[Resolved]) -> List[List[Resolved]]:
    """
    Creates small packets of files to process.
    """
    with ProcessPoolExecutor(max_workers=4) as executor:
        sizes = list(executor.map(get_size, all_resolved))

    packets: List[List[Reference]] = []
    packet: List[Reference] = []

    packet_size: int = 0
    total_size: int = 0

    for resolved, size in zip(all_resolved, sizes):
        if packet_size + size <= PACKET_SIZE:
            packet.append(resolved)
            packet_size += size
        else:
            packets.append(packet)
            packet = [resolved]
            packet_size = size
            total_size += packet_size

    if packet:
        packets.append(packet)
        total_size += packet_size

    print(f"Total content size: MB {total_size / 1024 / 1024:.2f}")
    return packets


def get_size(resolved: Resolved) -> int:
    """
    Get the size of a file.
    """
    return resolved.size_bytes


def process_packet(packet: List[Resolved]) -> List[Reference]:
    """
    Process a packet of files.
    """
    result: List[Reference] = []
    for resolved in packet:
        reference = resolved.create_reference()
        if reference:
            result.append(reference)

    return result


def create_remote_index(references: List[Reference], hashes: List[str]):
    """
    Create an index for a list of references.
    """
    missing_hashes: Set[str] = remote_get_unindexed_references(hashes).unindexed_hashes
    references_to_index: List[Reference] = [
        reference for reference in references if reference.hash in missing_hashes
    ]

    if references_to_index:
        remote_index_references(references_to_index)


def create_local_index(references: List[Reference], hashes: List[str]):
    """
    Create an index for a list of references.
    """
    missing_hashes: Set[str] = Index.get_missing_hashes(hashes)
    references_to_index: List[Reference] = [
        reference for reference in references if reference.hash in missing_hashes
    ]

    if references_to_index:
        Index.create_entries(references_to_index)
