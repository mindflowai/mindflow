class Reference: 
    def __init__(self, reference_hash, text, size, reference_type, path):
        self.hash = reference_hash
        self.text = text
        self.size = size
        self.type = reference_type
        self.path = path
    
    def get_type(self):
        return self.type
    
    def get_path(self):
        return self.path
