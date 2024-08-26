class BaseError(Exception):
    error_code: str
    error_message: str

    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(self.msg)

class NotFoundError(BaseError):
    pass

class AlreadyExistsError(BaseError):
    pass

class BadRequestError(BaseError):
    pass


class AccessDeniedError(BaseError):
    pass


class AuthenticationError(BaseError):
    pass