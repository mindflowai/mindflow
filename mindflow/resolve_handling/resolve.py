"""
Module for resolving references to text.
"""

from typing import List
from mindflow.resolve_handling.resolvers.path_resolver import PathResolver
from mindflow.resolve_handling.resolvers.base_resolver import Resolved


def resolve(reference: str) -> List[Resolved]:
    """
    Resolves a reference to text.
    """

    resolvers = [PathResolver()]
    for resolver in resolvers:
        if resolver.should_resolve(reference):
            return resolver.resolve(reference)

    raise ValueError(f"Cannot resolve reference: {reference}")
