"""
Base Resolver Class
"""


class BaseResolver:
    """
    Base class for resolvers
    """

    @staticmethod
    def should_resolve(document_path: str):
        """
        Checks if a string is a valid document path for this resolver.
        """

    @staticmethod
    def resolve(document_path: str):
        """
        Resolve a document path to text.
        """
