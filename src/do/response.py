from enum import Enum
from typing import Dict


class ResponseResult(Enum):
    ACCEPT = 'ACCEPT'
    REJECT = 'REJECT'


class PolicyValidationResponse:
    def __init__(self, result: ResponseResult, reason: str):
        self.result = result
        self.reason = reason

    def as_dict(self) -> Dict:
        return {
            'result': self.result.value,
            'reason': self.reason
        }
