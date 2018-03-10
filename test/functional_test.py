import json
import pytest
from app import app
from test.fixtures import db


def make_client():
    app.db = db()
    client = app.test_client()
    return client


@pytest.fixture
def get():
    client = make_client()

    def _get(url, headers=None, **kwargs):
        final_headers = {"API_KEY": "key1"}
        final_headers.update(headers or {})
        response = client.get(url, headers=final_headers, **kwargs)
        return json.loads(response.data)

    return _get


@pytest.fixture
def post():
    client = make_client()

    def _post(url, headers=None, data=None, **kwargs):
        final_headers = {"api-key": "key1", "content-type": "application/json"}
        final_headers.update(headers or {})
        kwargs.update({"headers": final_headers})
        kwargs.update({"data": json.dumps(data)})
        response = client.post(url, **kwargs)
        return json.loads(response.data)

    return _post


def test_set_api_key(get, post):
    assert get("/systems") == [1, 4]
    assert get("/systems", headers={"api-key": "the-new-key"}) == []

    assert post("/set-api-key", data={
        "new-api-key": "the-new-key"
    }) is True

    assert get("/systems") == []
    assert get("/systems", headers={"api-key": "the-new-key"}) == [1, 4]


def test_get_systems(get):
    assert get("/systems") == [1, 4]
    assert get("/systems", headers={"api-key": "key2"}) == [2]
    assert get("/systems", headers={"api-key": "key17"}) == []


def test_systems_specific(get):
    assert get("/systems/1") == {
        'armies': {"earth": 2},
        'controller': 1,
        'names': [],
        'owner-information': {'tuning-parameters': [], 'tuning_destinations': []},
        'production': 1,
        'routes': [{'destination': [4], 'distance': 1}]
    }
    assert get("/systems/2") == None
    assert get("/systems/4") == {
        'armies': {"earth": 1, "venus": 1},
        'controller': 1,
        'names': ["war"],
        'owner-information': {'tuning-parameters': [], 'tuning_destinations': []},
        'production': 1,
        'routes': [{'destination': [1], 'distance': 1},
                   {'destination': [2], 'distance': 2},
                   {'destination': [3], 'distance': 5}]
    }


pytest.main(["-vv"])
