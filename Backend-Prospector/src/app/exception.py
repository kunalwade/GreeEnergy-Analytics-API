class BaseAPIException(Exception):
    message = "Something went wrong!"
    code = None

    def __init__(self, message=None, code=None, details=None):
        self.message = message if message else self.message
        self.code = code if code else self.code
        self.details = details
        super().__init__(self.message)


class ResourceNotFoundException(BaseAPIException):
    message = "Resource not found"
    code = 404
