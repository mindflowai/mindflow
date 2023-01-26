"""
Helper module.
"""

class IndexType:
    """
    Index type enum.
    """

    DEEP: str = "deep"
    SHALLOW: str = "shallow"


def index_type(deep_index: bool):
    """
    Return the index type you may generate
    """
    if deep_index:
        return IndexType.DEEP
    return IndexType.SHALLOW
