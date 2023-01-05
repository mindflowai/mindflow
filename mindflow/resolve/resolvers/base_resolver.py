"""
Base Resolver Class
"""


class BaseResolver:
    """
    Base class for resolvers
    """

    def should_resolve(self, reference):
        """
        Checks if a string is a valid reference for this resolver.
        """

    def resolve(self, reference):
        """
        Resolve a reference to text.
        """

class Resolved: 
    """
    Base class for resolved references.
    """
    path: str
    type: str

    def create_reference(self):
        """
        Create a reference to a file or directory.
        """
    
    @property
    def size_bytes(self) -> str:
        """
        File size in bytes.
        """
    
    @property
    def text_hash(self) -> str:
        """
        File hash.
        """