def set_object_params(self, params: dict):
    for key, value in params.items():
        setattr(self, key, value)
    return self
