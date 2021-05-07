import pytest

from src.main import app
from src.do.response import ResponseResult


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_validate_success(client):
    response = client.post('/validate', json={
        'customer_income': 1000,
        'customer_debt': 500,
        'payment_remarks_12m': 0,
        'payment_remarks': 1,
        'customer_age': 18
    })
    assert response.status_code == 200
    assert response.get_json()['result'] == ResponseResult.ACCEPT.value


def test_validate_error_400(client):
    response = client.post('/validate', json={})
    assert response.status_code == 400
