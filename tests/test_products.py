"""
Products tests

Tests of the health check and the product endpoints.

@author adrianpmdev
"""


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_creating_a_product_returns_201_and_the_unchecked_product(client):
    response = client.post("/products", json={"name": "Desk lamp", "url": "https://shop.test/lamp"})

    assert response.status_code == 201
    product = response.json()
    assert product["name"] == "Desk lamp"
    assert product["is_broken"] is False
    assert product["last_checked_at"] is None


def test_creating_a_product_with_an_invalid_url_returns_422(client):
    response = client.post("/products", json={"name": "Desk lamp", "url": "not-a-url"})

    assert response.status_code == 422
