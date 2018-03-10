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
    return http_action_fixture(lambda client, url, **kwargs: client.get(url, **kwargs))


@pytest.fixture
def post():
    return http_action_fixture(lambda client, url, **kwargs: client.post(url, **kwargs))


@pytest.fixture
def delete():
    return http_action_fixture(lambda client, url, **kwargs: client.delete(url, **kwargs))


def http_action_fixture(client_func):
    client = make_client()

    def action(url, headers=None, data=None, **kwargs):
        final_headers = {"api-key": "key1", "content-type": "application/json"}
        final_headers.update(headers or {})
        kwargs.update({"headers": final_headers})
        if data:
            kwargs.update({"data": json.dumps(data)})
        response = client_func(client, url, **kwargs)
        return json.loads(response.data)

    return action


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
        "id": 1,
        'armies': {"earth": 2},
        'controller': 1,
        'names': [],
        'owner-information': {'tuning-parameters': [], 'tuning_destinations': []},
        'production': 1,
        'routes': [{'destination': [4], 'distance': 1}]
    }
    assert get("/systems/2") == None
    assert get("/systems/4") == {
        "id": 4,
        'armies': {"earth": 1, "venus": 1},
        'controller': 1,
        'names': ["war"],
        'owner-information': {'tuning-parameters': [], 'tuning_destinations': []},
        'production': 1,
        'routes': [{'destination': [1], 'distance': 1},
                   {'destination': [2], 'distance': 2},
                   {'destination': [3], 'distance': 5}]
    }


def test_system_names(get):
    assert get("/systems/names/3", {"api-key": "doesn't matter"}) == ["home", "venus"]
    assert get("/systems/names/1", {"api-key": "doesn't matter"}) == []
    assert get("/systems/names/12345", {"api-key": "doesn't matter"}) == None


def test_system_put_convenience_name(get, post):
    assert get("/systems/names/1", {"api-key": "doesn't matter"}) == []
    assert post("/systems/1/add-name/planet", {"api-key": "doesn't matter"}) == None
    assert get("/systems/names/1", {"api-key": "doesn't matter"}) == ["planet"]


def test_system_orders(get, post, delete):
    order1 = {"order": "repair-mode"}
    order2 = {"order": "transit-mode"}
    order3 = {"order": "abandon"}
    order4 = {"order": "build", "count": 1, "civ": [1]}

    def system_1_orders():
        return get("/system/1/orders")

    assert system_1_orders() == []
    post("/system/1/orders", data=order1)
    assert system_1_orders() == [order1]

    post("/system/1/orders", data=order2)
    assert system_1_orders() == [order1, order2]

    post("/system/1/orders", data=order3)
    assert system_1_orders() == [order1, order2, order3]

    post("/system/1/orders", data=order4)
    assert system_1_orders() == [order1, order2, order3, order4]

    delete("/system/1/orders/1")
    assert system_1_orders() == [order1, order3, order4]

    delete("/system/1/orders")
    assert system_1_orders() == []


def test_ship_orders(get, post):
    order1 = {"order": "suicide"}

    assert get("/ship/1/orders") == []
    post("/ship/1/orders", data=order1)
    assert get("/ship/1/orders") == [order1]


def test_get_ships(get, post):
    assert get("/ships") == [
        {'flag': 1, 'id': 1, 'location': 1, 'orders': [], 'shipyard': 1},
        {'flag': 1, 'id': 2, 'location': 1, 'orders': [], 'shipyard': 1},
        {'flag': 1, 'id': 3, 'location': 4, 'orders': [], 'shipyard': 1}
    ]

    assert get("/ships", {"api-key": "key2"}) == []

    assert get("/ships", {"api-key": "key3"}) == [
        {'flag': 3, "id": 4, "location": 4, "orders": [], "shipyard": 3}
    ]

    assert post("/ship/4/orders",
                headers={"api-key": "key3"},
                data={"order": "suicide"}) is True
    assert get("/ships", {"api-key": "key3"}) == [
        {'flag': 3, "id": 4, "location": 4, "orders": [{"order": "suicide"}], "shipyard": 3}
    ]
