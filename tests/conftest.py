"""
Conftest

Test fixtures: a temporary database, a test client that never starts the
scheduler and fake outgoing HTTP calls, so tests never hit the network.

@author adrianpmdev
"""

from types import SimpleNamespace

import pytest
import requests
from fastapi.testclient import TestClient

from app import checker, config
from app.database import init_db
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DB_PATH", tmp_path / "test.db")
    monkeypatch.setattr(config, "SEED_SAMPLE_DATA", False)
    init_db()
    # Not used as a context manager, so the lifespan (and the scheduler) does not run.
    return TestClient(app)


@pytest.fixture
def fake_http(monkeypatch):
    """Status codes per URL for HEAD and GET. A URL that is not listed is unreachable."""
    responses = SimpleNamespace(head={}, get={})

    def respond(codes: dict[str, int], url: str) -> SimpleNamespace:
        if url not in codes:
            raise requests.ConnectionError(f"Cannot reach {url}")
        return SimpleNamespace(status_code=codes[url])

    monkeypatch.setattr(checker.requests, "head", lambda url, **_: respond(responses.head, url))
    monkeypatch.setattr(checker.requests, "get", lambda url, **_: respond(responses.get, url))
    return responses
