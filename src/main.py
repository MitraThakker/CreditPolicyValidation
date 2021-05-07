import os

import yaml
from flask import Flask, request

from src.do.request import PolicyValidationRequest
from src.service.helpers import read_yaml
from src.service.policy_validation import PolicyValidationService

app = Flask('__main__')


@app.route('/validate', methods=['POST'])
def validate():
    try:
        request_ = PolicyValidationRequest.from_dict(request.get_json(force=True))
        validation_config = read_yaml(f'{os.path.dirname(__file__)}/service/validation_config.yaml')
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


if __name__ == '__main__':
    app.run()
