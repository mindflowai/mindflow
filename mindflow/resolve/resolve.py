from mindflow.resolve.resolvers.path_resolver import PathResolver

def resolve(reference):
    """
    Resolves a reference to text.
    """
    
    resolvers = [PathResolver(reference)]
    for resolver in resolvers:
        if resolver.should_resolve():
            return resolver.resolve()

    raise ValueError(f"Cannot resolve reference: {reference}")
