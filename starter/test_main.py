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
    r = client.post("/shorten", json={"url": "https://alias-test.com", "alias": "mylink"})
    assert r.status_code == 200
    data = r.json()
    assert data["code"] == "mylink"
    assert data["short_url"] == "/mylink"
    r2 = client.get("/mylink", follow_redirects=False)
    assert r2.status_code == 307
    assert r2.headers["location"] == "https://alias-test.com"


def test_custom_alias_conflict():
    # First registration must succeed
    client.post("/shorten", json={"url": "https://first.com", "alias": "taken"})
    # Second registration with same alias must return 409
    r = client.post("/shorten", json={"url": "https://second.com", "alias": "taken"})
    assert r.status_code == 409


def test_blank_alias_rejected():
    r = client.post("/shorten", json={"url": "https://example.com", "alias": ""})
    assert r.status_code == 400
