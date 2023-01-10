"""
Class for references to be sent to backend.
"""

class Reference:
    """
    Reference Class.
    """
    def __init__(self, reference_hash, text, size, reference_type, path):
        self.hash = reference_hash
        self.text = text
        self.size = size
        self.type = reference_type
        self.path = path
