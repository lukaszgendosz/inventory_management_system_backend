from enum import Enum, auto


class ErrorMessage(Enum):
    code: str
    description: str

    def __new__(cls, code, description):
        obj = object.__new__(cls)
        obj._value_ = auto()
        obj.code = code
        obj.description = description
        return obj

    SOMETHING_WENT_WRONG = (
        "something_went_wrong",
        "Something went wrong during processing request.",
    )
    VALIDATION_FAILED = ("unprocessable_entity", "Cannot process the request.")
