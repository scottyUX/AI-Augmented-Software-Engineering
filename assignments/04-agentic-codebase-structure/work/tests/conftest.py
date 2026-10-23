import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client(tmp_path, monkeypatch):
    """A TestClient backed by a fresh, empty SQLite file for every test."""
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "links.db")
    main.init_db()
    return TestClient(main.app)


@pytest.fixture
def shorten(client):
    """Shorten a URL through the API and return its code."""
    def _shorten(url="https://example.com"):
        r = client.post("/shorten", json={"url": url})
        assert r.status_code == 200
        return r.json()["code"]
    return _shorten
