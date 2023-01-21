"""
Request to index references.
"""

import json
from typing import List
import requests

from mindflow.utils.config import config as Config
from mindflow.utils.reference import Reference


class IndexReferenceRequest:
    """
    Index request object.
    """

    references: str = None
    auth: str = None

    def __init__(self, unindexed_references: List[Reference], auth: str):
        self.references = json.dumps(
            [vars(unindexed_reference) for unindexed_reference in unindexed_references]
        )
        self.auth = auth


def index_references(unindexed_references: List[Reference]) -> None:
    """
    This function makes a post request to the backend to index the unindexed references.
    """
    response = requests.post(
        f"{Config.API_LOCATION}/index",
        json=vars(IndexReferenceRequest(unindexed_references, Config.mindflow_auth())),
        timeout=10,
    )
    if response.status_code != 200:
        print(f"Error: {response.status_code} {response.text}")
