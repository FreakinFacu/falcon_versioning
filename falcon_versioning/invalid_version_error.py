class InvalidVersionError(Exception):
    def __init__(self, invalid_version):
        self.invalid_version = invalid_version
