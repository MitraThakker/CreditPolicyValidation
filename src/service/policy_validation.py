from typing import Dict

from src.do.request import PolicyValidationRequest
from src.do.response import PolicyValidationResponse, ResponseResult
from src.service.helpers import validate_config


class PolicyValidationService:
    def __init__(self, request: PolicyValidationRequest, config: Dict):
        self.request = request
        self.config = config

    @validate_config
    def is_acceptable_income(self, customer_income: float) -> bool:
        return customer_income >= float(self.config['minimum_customer_income']['threshold'])

    @validate_config
    def is_acceptable_debt(self, customer_income: float, customer_debt: float) -> bool:
        return customer_debt <= customer_income * float(self.config['maximum_customer_debt']['threshold'])

    @validate_config
    def is_acceptable_payment_remarks_12m(self, payment_remarks_12m: int) -> bool:
        return payment_remarks_12m <= int(self.config['maximum_payment_remarks_12m']['threshold'])

    @validate_config
    def is_acceptable_payment_remarks(self, payment_remarks: int) -> bool:
        return payment_remarks <= int(self.config['maximum_payment_remarks']['threshold'])

    @validate_config
    def is_acceptable_customer_age(self, customer_age: int) -> bool:
        return customer_age >= int(self.config['minimum_customer_age']['threshold'])

    @validate_config
    def run(self) -> PolicyValidationResponse:
        if not self.is_acceptable_income(self.request.customer_income):
            return PolicyValidationResponse(result=ResponseResult.REJECT,
                                            reason=self.config['minimum_customer_income']['rejection_reason'])

        if not self.is_acceptable_debt(self.request.customer_income, self.request.customer_debt):
            return PolicyValidationResponse(result=ResponseResult.REJECT,
                                            reason=self.config['maximum_customer_debt']['rejection_reason'])

        if not self.is_acceptable_payment_remarks_12m(self.request.payment_remarks_12m):
            return PolicyValidationResponse(result=ResponseResult.REJECT,
                                            reason=self.config['maximum_payment_remarks_12m']['rejection_reason'])

        if not self.is_acceptable_payment_remarks(self.request.payment_remarks):
            return PolicyValidationResponse(result=ResponseResult.REJECT,
                                            reason=self.config['maximum_payment_remarks']['rejection_reason'])

        if not self.is_acceptable_customer_age(self.request.customer_age):
            return PolicyValidationResponse(result=ResponseResult.REJECT,
                                            reason=self.config['minimum_customer_age']['rejection_reason'])

        return PolicyValidationResponse(result=ResponseResult.ACCEPT,
                                        reason='')
