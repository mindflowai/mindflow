"""
Contains the resolve function for resolving references to text.
"""
from mindflow.resolve.resolvers.path_resolver import PathResolver
from mindflow.resolve.resolvers.url_resolver import URLResolver


def resolve(reference, model, prompt):
    """
    Resolves a reference to text.
    """
    resolvers = [PathResolver(reference, model, prompt), URLResolver(reference)]
    for resolver in resolvers:
        if resolver.should_resolve():
            return resolver.resolve()

    raise ValueError(f"Cannot resolve reference: {reference}")
