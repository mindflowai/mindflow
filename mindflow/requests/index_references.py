"""
Request to index references.
"""

import json
from typing import List
import requests

from mindflow.utils.config import Config
from mindflow.utils.reference import Reference


def request_index_references(
    resolved_references: dict[str, Reference], unindexed_hashes: List[str]
):
    """
    This function makes a post request to the backend to index the unindexed references.
    """
    if len(unindexed_hashes) == 0:
        return
    unindexed_references: List[Reference] = [
        vars(resolved_references[unindexed_reference])
        for unindexed_reference in unindexed_hashes
    ]
    response = requests.post(
        f"{Config.API_LOCATION}/index",
        json={"references": json.dumps(unindexed_references), "auth": Config.AUTH},
        timeout=10,
    )
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")
