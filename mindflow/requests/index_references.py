"""
Request to index references.
"""

import json
import requests

from mindflow.utils.config import Config
from mindflow.utils.reference import Reference


def request_index_references(
    resolved_references: dict[str, Reference], unindexed_hashes: list
):
    """
    This function makes a post request to the backend to index the unindexed references.
    """
    if len(unindexed_hashes) == 0:
        return
    unindexed_references = [
        resolved_references[unindexed_reference].__dict__
        for unindexed_reference in unindexed_hashes
    ]
    response = requests.post(
        f"{Config.API_LOCATION}/index",
        json={"references": json.dumps(unindexed_references), "auth": Config.AUTH},
        timeout=10,
    )
    if response.status_code != 200:
        raise ValueError(f"Error: {response.status_code} {response.text}")
