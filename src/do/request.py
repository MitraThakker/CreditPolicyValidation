from typing import Dict


class PolicyValidationRequest:
    def __init__(self,
                 customer_income: float,
                 customer_debt: float,
                 payment_remarks_12m: int,
                 payment_remarks: int,
                 customer_age: int):
        self.customer_income = customer_income
        self.customer_debt = customer_debt
        self.payment_remarks_12m = payment_remarks_12m
        self.payment_remarks = payment_remarks
        self.customer_age = customer_age

    @staticmethod
    def from_dict(dict_: Dict):
        return PolicyValidationRequest(customer_income=float(dict_['customer_income']),
                                       customer_debt=float(dict_['customer_debt']),
                                       payment_remarks_12m=int(dict_['payment_remarks_12m']),
                                       payment_remarks=int(dict_['payment_remarks']),
                                       customer_age=int(dict_['customer_age']))
