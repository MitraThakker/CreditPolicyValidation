from typing import Dict


class PolicyValidationRequest:
    """
    The plain Python object corresponding to the JSON request body.
    It gives a better structure and type-checking to work with compared to a simple dictionary.
    It is also easier to add methods around the request for future enhancements on the object.
    In a real-world application, this could be a Model object that could work well with
    ORMs when using with frameworks like Django/Flask.
    """

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
        """
        Method to construct a `PolicyValidationRequest` object from a dictionary object.
        This method will raise a `KeyError` or `ValueError` in case a field is missing or
        has an incompatible value that can't be type-casted to the desired data type.
        """
        return PolicyValidationRequest(customer_income=float(dict_['customer_income']),
                                       customer_debt=float(dict_['customer_debt']),
                                       payment_remarks_12m=int(dict_['payment_remarks_12m']),
                                       payment_remarks=int(dict_['payment_remarks']),
                                       customer_age=int(dict_['customer_age']))
