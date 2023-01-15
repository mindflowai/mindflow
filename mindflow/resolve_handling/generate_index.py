"""
Generate an index for a list of resolved paths.
"""

from asyncio import Future
from typing import List
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

from alive_progress import alive_bar

from mindflow.requests.unindexed_reference import request_unindexed_references
from mindflow.requests.index_references import request_index_references
from mindflow.resolve_handling.resolvers.base_resolver import Resolved
from mindflow.utils.reference import Reference

PACKET_SIZE = 2 * 1024 * 1024


def generate_index(all_resolved: List[Resolved]):
    """
    Generate an index for a list of resolved paths.
    """

    packets: List[Resolved] = create_packets(all_resolved)

    # Create a thread pool with 4 worker threads
    with ThreadPoolExecutor(max_workers=500) as executor:
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

                unindexed_hashes: List[str] = request_unindexed_references(hashes)
                if unindexed_hashes:
                    request_index_references(
                        {r.hash: r for r in references}, unindexed_hashes
                    )

                progress_bar(len(references))


def create_packets(all_resolved: List[Resolved]) -> List[List[Resolved]]:
    """
    Creates small packets of files to process.
    """
    with ProcessPoolExecutor(max_workers=50) as executor:
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
            total_size += packet_size
            packet_size = size

    if packet:
        total_size += packet_size
        packets.append(packet)

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
