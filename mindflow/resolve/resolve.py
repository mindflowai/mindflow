from mindflow.resolve.resolvers.git_resolver import GitResolver
from mindflow.resolve.resolvers.path_resolver import PathResolver
from mindflow.resolve.resolvers.url_resolver import URLResolver


def resolve(reference, model, prompt):
    """
    Resolves a reference to text.
    """
    
    resolvers = [GitResolver(reference), PathResolver(reference, model, prompt), URLResolver(reference)]
    for resolver in resolvers:
        if resolver.should_resolve():
            return resolver.resolve()

    raise ValueError(f"Cannot resolve reference: {reference}")


def parallel_resolve(references, model, prompt):
    """
    Resolves a list of references to text.
    """

    raise NotImplementedError
    return [resolve(reference, model, prompt) for reference in references]