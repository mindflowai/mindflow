"""
Generate an index for a list of resolved paths.
"""

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from mindflow.requests.unindexed_reference import request_unindexed_references
from mindflow.requests.index_references import request_index_references
from mindflow.resolve.resolvers.base_resolver import Resolved

PACKET_SIZE = 2 * 1024 * 1024

def get_size(resolved_path):
    """
    Get the size of a file.
    """
    return resolved_path.size_bytes

def process_packet(packet):
    """
    Process a packet of files.
    """
    result = []
    for resolved_path in packet:
        reference = resolved_path.create_reference()
        if reference:
            result.append(reference)

    return result

def generate_index(resolved_paths: list[Resolved]):
    """
    Generate an index for a list of resolved paths.
    """
    processed_hashes = []

    with ProcessPoolExecutor(max_workers=50) as executor:
        sizes = list(executor.map(get_size, resolved_paths))

    packets = []
    packet = []

    size = 0
    total_size = 0

    for file_path, file_size in zip(resolved_paths, sizes):
        if size + file_size <= PACKET_SIZE:
            packet.append(file_path)
            size += file_size
        else:
            packets.append(packet)
            packet = [file_path]
            total_size += size
            size = file_size

    if packet:
        total_size += size
        packets.append(packet)

    # Create a thread pool with 4 worker threads
    with ThreadPoolExecutor(max_workers=500) as executor:
        # Submit the tasks to the thread pool
        results = [executor.submit(process_packet, packet) for packet in packets]

        # Process the results as they complete
        processed_hashes = []
        for f in as_completed(results):
            result = f.result()
            hashes = [reference.hash for reference in result]
            unindexed_hashes = request_unindexed_references(hashes)
            request_index_references({r.hash: r for r in result}, unindexed_hashes)
            processed_hashes.extend(hashes)

    print(f'Total content size: MB {total_size / 1024 / 1024:.2f}')
    return hashes
