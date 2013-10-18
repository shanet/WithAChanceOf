class GenericError(Exception):
    def __init__(self, message=None, errno=0):
        Exception.__init__(self)
        self.message = message
        self.errno   = errno


class LocationNotFoundError(GenericError):
    def __init__(self, message=None, errno=0):
        GenericError.__init__(self, message, errno)


class GetForecastError(GenericError):
    def __init__(self, message=None, errno=0):
        GenericError.__init__(self, message, errno)
