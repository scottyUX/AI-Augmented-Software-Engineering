import uuid
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_shorten_and_redirect():
    r = client.post("/shorten", json={"url": "https://example.com"})
    assert r.status_code == 200
    code = r.json()["code"]
    assert code
    r2 = client.get(f"/{code}", follow_redirects=False)
    assert r2.status_code == 307
    assert r2.headers["location"] == "https://example.com"


def test_rejects_bad_url():
    r = client.post("/shorten", json={"url": "ftp://nope"})
    assert r.status_code == 400


def test_unknown_code_404():
    r = client.get("/does-not-exist", follow_redirects=False)
    assert r.status_code == 404


def test_custom_alias_success():
    alias = f"custom-{uuid.uuid4().hex[:8]}"
    r = client.post("/shorten", json={"url": "https://example.com/custom", "alias": alias})
    assert r.status_code == 200
    data = r.json()
    assert data["code"] == alias
    assert data["short_url"] == f"/{alias}"

    r2 = client.get(f"/{alias}", follow_redirects=False)
    assert r2.status_code == 307
    assert r2.headers["location"] == "https://example.com/custom"


def test_custom_alias_duplicate_conflict_409():
    alias = f"dup-{uuid.uuid4().hex[:8]}"
    r1 = client.post("/shorten", json={"url": "https://example.com/first", "alias": alias})
    assert r1.status_code == 200

    r2 = client.post("/shorten", json={"url": "https://example.com/second", "alias": alias})
    assert r2.status_code == 409
    assert "taken" in r2.json()["detail"].lower()
