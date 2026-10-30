from uuid import uuid4

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


def test_custom_alias_shortens_and_redirects():
    alias = f"docs-{uuid4().hex}"
    r = client.post(
        "/shorten",
        json={"url": "https://example.com/docs", "alias": alias},
    )

    assert r.status_code == 200
    assert r.json() == {"code": alias, "short_url": f"/{alias}"}

    redirect_response = client.get(f"/{alias}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://example.com/docs"


def test_custom_alias_conflict_returns_409():
    alias = f"duplicate-{uuid4().hex}"
    payload = {"url": "https://example.com", "alias": alias}

    first = client.post("/shorten", json=payload)
    second = client.post("/shorten", json=payload)

    assert first.status_code == 200
    assert second.status_code == 409
