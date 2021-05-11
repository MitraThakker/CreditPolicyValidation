from typing import Dict

from src.do.request import PolicyValidationRequest
from src.do.response import PolicyValidationResponse, ResponseResult
from src.service.helpers import validate_config


class PolicyValidationService:
    """
    This is where the business logic resides to validate the customer details based on
    the defined credit policies. The constructor accepts a `PolicyValidationRequest` object
    and a dictionary containing the validation config. Executing the `run()` method should
    run all the validations in the appropriate sequence and return the final response.
    """

    def __init__(self, request: PolicyValidationRequest, config: Dict):
        self.request = request
        self.config = config

    @validate_config
    def is_acceptable_income(self, customer_income: float) -> bool:
        """
        Validates if the customer's income is above the defined threshold.
        """
        return customer_income >= float(self.config['minimum_customer_income']['threshold'])

    @validate_config
    def is_acceptable_debt(self, customer_income: float, customer_debt: float) -> bool:
        """
        Validates if the customer's debt is below the defined threshold compared to their income.
        """
        return customer_debt <= customer_income * float(self.config['maximum_customer_debt']['threshold'])

    @validate_config
    def is_acceptable_payment_remarks_12m(self, payment_remarks_12m: int) -> bool:
        """
        Validates if the customer's payment remarks in the last 2 months are
        below the defined threshold.
        """
        return payment_remarks_12m <= int(self.config['maximum_payment_remarks_12m']['threshold'])

    @validate_config
    def is_acceptable_payment_remarks(self, payment_remarks: int) -> bool:
        """
        Validates if the customer's payment remarks are below the defined threshold.
        """
        return payment_remarks <= int(self.config['maximum_payment_remarks']['threshold'])

    @validate_config
    def is_acceptable_customer_age(self, customer_age: int) -> bool:
        """
        Validates if the customer's age is above the defined threshold
        """
        return customer_age >= int(self.config['minimum_customer_age']['threshold'])

    @validate_config
    def run(self) -> PolicyValidationResponse:
        """
        Runs all validations necessary as per the credit policy and
        returns a `PolicyValidationResponse` object with the appropriate values.
        """
        reasons = []
        if not self.is_acceptable_income(self.request.customer_income):
            reasons.append(self.config['minimum_customer_income']['rejection_reason'])

        if not self.is_acceptable_debt(self.request.customer_income, self.request.customer_debt):
            reasons.append(self.config['maximum_customer_debt']['rejection_reason'])

        if not self.is_acceptable_payment_remarks_12m(self.request.payment_remarks_12m):
            reasons.append(self.config['maximum_payment_remarks_12m']['rejection_reason'])

        if not self.is_acceptable_payment_remarks(self.request.payment_remarks):
            reasons.append(self.config['maximum_payment_remarks']['rejection_reason'])

        if not self.is_acceptable_customer_age(self.request.customer_age):
            reasons.append(self.config['minimum_customer_age']['rejection_reason'])

        result = ResponseResult.REJECT if reasons else ResponseResult.ACCEPT
        return PolicyValidationResponse(result=result, reasons=reasons)
