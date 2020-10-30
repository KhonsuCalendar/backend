from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)


def test_hello_world():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'hello, world'}


def test_phase_missing_date_gets_created():
    response = client.post('/event/', json={"phase": "full", "datetime": "2020-10-23T00:08:38.852Z", "cycle": 1})
    assert response.status_code == 200
    assert 'id' in response.json().keys()


def test_phase_missing_date_doesnt_get_created():
    response = client.post('/event/', json={"phase": "full", "cycle": 1})
    assert response.status_code == 422
    assert 'id' not in response.json().keys()
