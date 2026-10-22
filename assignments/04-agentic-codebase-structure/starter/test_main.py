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
    r = client.post("/shorten", json={"url": "https://example.com", "alias": "my-alias"})
    assert r.status_code == 200
    assert r.json()["code"] == "my-alias"
    assert r.json()["short_url"] == "/my-alias"
    r2 = client.get("/my-alias", follow_redirects=False)
    assert r2.status_code == 307
    assert r2.headers["location"] == "https://example.com"


def test_custom_alias_conflict():
    r = client.post("/shorten", json={"url": "https://example.com", "alias": "taken-alias"})
    assert r.status_code == 200
    r_conflict = client.post("/shorten", json={"url": "https://other.com", "alias": "taken-alias"})
    assert r_conflict.status_code == 409

