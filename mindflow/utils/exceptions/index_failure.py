class IndexGenerationFailure(Exception):
    def __init__(self, message):
        super().__init__(message)

class FailureToTrimFiles(Exception):
    def __init__(self, message):
        super().__init__(message)