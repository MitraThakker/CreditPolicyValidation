from enum import Enum
from typing import Dict


class ResponseResult(Enum):
    """
    This Enum for the result values makes re-factoring easier in the future
    and keeps the values consistent across the application instead of hard-coded strings.
    """
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'


class PolicyValidationResponse:
    """
    The plain Python object corresponding to the JSON response body.
    It gives a better structure and type-checking to work with compared to a simple dictionary.
    It is also easier to add methods around the response for future enhancements on the object.
    In a real-world application, this could be a Model object that could work well with
    ORMs when using with frameworks like Django/Flask.
    """

    def __init__(self, result: ResponseResult, reason: str):
        self.result = result
        self.reason = reason

    def as_dict(self) -> Dict:
        """
        Method to construct a dictionary object from a `PolicyValidationResponse` object.
        """
        return {
            'result': self.result.value,
            'reason': self.reason
        }
