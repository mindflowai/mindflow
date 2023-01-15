"""
Base Resolver Class
"""


class BaseResolver:
    """
    Base class for resolvers
    """

    def should_resolve(self, reference: str):
        """
        Checks if a string is a valid reference for this resolver.
        """

    def resolve(self, reference: str):
        """
        Resolve a reference to text.
        """


class Resolved:
    """
    Base class for resolved references.
    """

    path: str

    def create_reference(self):
        """
        Create a reference to a file or directory.
        """

    @property
    def type(self) -> str:
        """
        Type.
        """

    @property
    def size_bytes(self) -> int:
        """
        Size in bytes.
        """

    @property
    def text_hash(self) -> str:
        """
        Text hash.
        """
