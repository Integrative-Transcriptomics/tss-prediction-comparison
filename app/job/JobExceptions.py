class NotReadyException(Exception):
    def __init__(self, message):
        self.message = message


class NotSuppliedException(Exception):
    def __init__(self, message):
        self.message = message