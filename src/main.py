import os

import yaml
from flask import Flask, request

from src.do.request import PolicyValidationRequest
from src.service.helpers import read_yaml
from src.service.policy_validation import PolicyValidationService

app = Flask('CreditPolicyValidation')


@app.route('/validate', methods=['POST'])
def validate():
    """
    API endpoint to validate the customer details based on the defined credit policies.

    Sample Request:
        {
            "customer_income": 1000,
            "customer_debt": 500,
            "payment_remarks_12m": 0,
            "payment_remarks": 1,
            "customer_age": 18
        }

    Sample Response:
        {
            "reason": "",
            "result": "ACCEPT"
        }
    """
    try:
        request_ = PolicyValidationRequest.from_dict(request.get_json(force=True))
        validation_config = read_yaml(os.environ['VALIDATION_CONFIG_PATH'])
        response_ = PolicyValidationService(request_, validation_config).run()
        return response_.as_dict(), 200
    except (KeyError, ValueError):
        # KeyError will be raised if any of the mandatory keys are absent in the request
        # ValueError will be raised if any of the request attribute values can't be cast into their data type
        # The above errors indicate a bad request and thus, the status code is set to 400 here
        return {
                   'error': 'Error parsing request. Please check the request attributes and their types.'
               }, 400
    except yaml.YAMLError:
        return {
                   'error': 'Error parsing YAML file containing policy validation config.'
               }, 500
