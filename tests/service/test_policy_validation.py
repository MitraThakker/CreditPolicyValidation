import unittest

import yaml

from src.do.request import PolicyValidationRequest
from src.do.response import ResponseResult
from src.service.policy_validation import PolicyValidationService


class TestPolicyValidationService(unittest.TestCase):

    def setUp(self):
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

    def tearDown(self):
        pass

    def test_run_accept(self):
        request_ = PolicyValidationRequest(customer_income=1000,
                                           customer_debt=500,
                                           payment_remarks_12m=0,
                                           payment_remarks=1,
                                           customer_age=18)
        response_ = PolicyValidationService(request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.ACCEPT.value, response_.get('result'))
        self.assertEqual('', response_.get('reason'))

    def test_low_income(self):
        request_ = PolicyValidationRequest(customer_income=499,
                                           customer_debt=500,
                                           payment_remarks_12m=0,
                                           payment_remarks=1,
                                           customer_age=18)
        response_ = PolicyValidationService(request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual('LOW_INCOME', response_.get('reason'))

    def test_high_debt(self):
        request_ = PolicyValidationRequest(customer_income=1000,
                                           customer_debt=501,
                                           payment_remarks_12m=0,
                                           payment_remarks=1,
                                           customer_age=18)
        response_ = PolicyValidationService(request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual('HIGH_DEBT_FOR_INCOME', response_.get('reason'))

    def test_payment_remarks_12m(self):
        request_ = PolicyValidationRequest(customer_income=1000,
                                           customer_debt=500,
                                           payment_remarks_12m=1,
                                           payment_remarks=1,
                                           customer_age=18)
        response_ = PolicyValidationService(request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual('PAYMENT_REMARKS_12M', response_.get('reason'))

    def test_payment_remarks(self):
        request_ = PolicyValidationRequest(customer_income=1000,
                                           customer_debt=500,
                                           payment_remarks_12m=0,
                                           payment_remarks=2,
                                           customer_age=18)
        response_ = PolicyValidationService(request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual('PAYMENT_REMARKS', response_.get('reason'))

    def test_underage(self):
        request_ = PolicyValidationRequest(customer_income=1000,
                                           customer_debt=500,
                                           payment_remarks_12m=0,
                                           payment_remarks=1,
                                           customer_age=17)
        response_ = PolicyValidationService(request_, self.base_config).run().as_dict()

        self.assertEqual(ResponseResult.REJECT.value, response_.get('result'))
        self.assertEqual('UNDERAGE', response_.get('reason'))

    def test_invalid_config(self):
        request_ = PolicyValidationRequest(customer_income=1000,
                                           customer_debt=500,
                                           payment_remarks_12m=0,
                                           payment_remarks=1,
                                           customer_age=18)
        with self.assertRaises(yaml.YAMLError):
            PolicyValidationService(request_, {}).run().as_dict()


if __name__ == '__main__':
    unittest.main()
