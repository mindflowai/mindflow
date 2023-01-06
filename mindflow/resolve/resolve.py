from mindflow.resolve.resolvers.path_resolver import PathResolver

def resolve(reference):
    """
    Resolves a reference to text.
    """
    
    resolvers = [PathResolver()]
    for resolver in resolvers:
        if resolver.should_resolve(reference):
            return resolver.resolve(reference)

    raise ValueError(f"Cannot resolve reference: {reference}")
