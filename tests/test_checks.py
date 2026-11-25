"""
Checks tests

Tests of the link check: broken link detection and the protection against
overlapping runs.

@author adrianpmdev
"""

from app import checker

OK_URL = "https://shop.test/ok"
MISSING_URL = "https://shop.test/missing"
UNREACHABLE_URL = "https://unreachable.test/item"


def add_product(client, name, url):
    return client.post("/products", json={"name": name, "url": url}).json()


def test_running_a_check_marks_error_and_unreachable_links_as_broken(client, fake_http):
    fake_http.head.update({OK_URL: 200, MISSING_URL: 404})
    add_product(client, "Lamp", OK_URL)
    add_product(client, "Chair", MISSING_URL)
    add_product(client, "Table", UNREACHABLE_URL)

    response = client.post("/checks/run")

    assert response.status_code == 200
    assert response.json() == {"checked": 3, "broken": 2}
    broken = {product["name"]: product for product in client.get("/products/broken").json()}
    assert set(broken) == {"Chair", "Table"}
    assert broken["Chair"]["status_code"] == 404
    assert broken["Table"]["status_code"] is None
    assert broken["Table"]["last_checked_at"] is not None


def test_running_a_check_while_another_is_running_returns_409(client, fake_http):
    with checker._run_lock:
        response = client.post("/checks/run")

    assert response.status_code == 409
