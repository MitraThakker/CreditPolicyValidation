import unittest

import yaml

from src.do.request import PolicyValidationRequest
from src.do.response import ResponseResult
from src.service.policy_validation import PolicyValidationService


class TestPolicyValidationService(unittest.TestCase):

    def setUp(self) -> None:
        self.base_config = {
            'minimum_customer_income': {
                'threshold': 500,
                'rejection_reason': 'LOW_INCOME'
            },
            'maximum_customer_debt': {
                'threshold': 0.5,
                'rejection_reason': 'HIGH_DEBT_FOR_INCOME'
            },
            'maximum_payment_remarks_12m': {
                'threshold': 0,
                'rejection_reason': 'PAYMENT_REMARKS_12M'
            },
            'maximum_payment_remarks': {
                'threshold': 1,
                'rejection_reason': 'PAYMENT_REMARKS'
            },
            'minimum_customer_age': {
                'threshold': 18,
                'rejection_reason': 'UNDERAGE'
            }
        }
        self.request_ = PolicyValidationRequest(customer_income=1000,
                                                customer_debt=500,
                                                payment_remarks_12m=0,
                                                payment_remarks=1,
                                                customer_age=18)

    def test_run_accept(self):
        response_ = PolicyValidationService(self.request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.ACCEPT.value, response_.get('result'))
        self.assertEqual(0, len(response_.get('reasons')))

    def test_low_income(self):
        self.request_.customer_income = 499.99
        self.request_.customer_debt = 0.0
        response_ = PolicyValidationService(self.request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual(1, len(response_.get('reasons')))
        self.assertEqual('LOW_INCOME', response_.get('reasons')[0])

    def test_high_debt(self):
        self.request_.customer_debt = 501
        response_ = PolicyValidationService(self.request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual(1, len(response_.get('reasons')))
        self.assertEqual('HIGH_DEBT_FOR_INCOME', response_.get('reasons')[0])

    def test_payment_remarks_12m(self):
        self.request_.payment_remarks_12m = 1
        response_ = PolicyValidationService(self.request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual(1, len(response_.get('reasons')))
        self.assertEqual('PAYMENT_REMARKS_12M', response_.get('reasons')[0])

    def test_payment_remarks(self):
        self.request_.payment_remarks = 2
        response_ = PolicyValidationService(self.request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual(1, len(response_.get('reasons')))
        self.assertEqual('PAYMENT_REMARKS', response_.get('reasons')[0])

    def test_underage(self):
        self.request_.customer_age = 17
        response_ = PolicyValidationService(self.request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual(1, len(response_.get('reasons')))
        self.assertEqual('UNDERAGE', response_.get('reasons')[0])

    def test_all_failure_reasons(self):
        self.request_ = PolicyValidationRequest(customer_income=499.99,
                                                customer_debt=500,
                                                payment_remarks_12m=1,
                                                payment_remarks=2,
                                                customer_age=17)
        response_ = PolicyValidationService(self.request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual(5, len(response_.get('reasons')))
        self.assertEqual('LOW_INCOME', response_.get('reasons')[0])
        self.assertEqual('HIGH_DEBT_FOR_INCOME', response_.get('reasons')[1])
        self.assertEqual('PAYMENT_REMARKS_12M', response_.get('reasons')[2])
        self.assertEqual('PAYMENT_REMARKS', response_.get('reasons')[3])
        self.assertEqual('UNDERAGE', response_.get('reasons')[4])

    def test_invalid_config(self):
        with self.assertRaises(yaml.YAMLError):
            PolicyValidationService(self.request_, {}).run()


if __name__ == '__main__':
    unittest.main()
