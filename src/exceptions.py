class PersistedQueryNotFoundError(Exception):
    message: str = "PersistedQueryNotFound"
    code: str = "PERSISTED_QUERY_NOT_FOUND"

    def __init__(self):
        super().__init__(self.code)
