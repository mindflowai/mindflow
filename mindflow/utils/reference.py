class Reference: 
    def __init__(self, hash, text, size, type, path):
        self.hash = hash
        self.text = text
        self.size = size
        self.type = type
        self.path = path
    
    def get_text(self):
        return self.text_bytes.decode("utf-8")
    
    def get_text_bytes(self):
        return self.text_bytes
    
    def get_type(self):
        return self.type
    
    def get_path(self):
        return self.path
