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


# --- Custom alias tests ---


def test_custom_alias_used_as_code():
    """Providing a valid alias returns that alias as the code and short_url."""
    alias = "alias-" + uuid.uuid4().hex[:8]
    r = client.post("/shorten", json={"url": "https://example.com", "alias": alias})
    assert r.status_code == 200
    assert r.json()["code"] == alias
    assert r.json()["short_url"] == f"/{alias}"


def test_custom_alias_redirects_correctly():
    """A custom alias resolves to the correct URL via redirect."""
    alias = "redir-" + uuid.uuid4().hex[:8]
    client.post("/shorten", json={"url": "https://target.example.com", "alias": alias})
    r = client.get(f"/{alias}", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "https://target.example.com"


def test_alias_already_taken_returns_409():
    """Re-using an alias that is already stored returns 409 Conflict."""
    alias = "taken-" + uuid.uuid4().hex[:8]
    client.post("/shorten", json={"url": "https://a.com", "alias": alias})
    r = client.post("/shorten", json={"url": "https://b.com", "alias": alias})
    assert r.status_code == 409


def test_empty_alias_returns_400():
    """An empty-string alias is invalid and returns 400."""
    r = client.post("/shorten", json={"url": "https://example.com", "alias": ""})
    assert r.status_code == 400


def test_alias_invalid_chars_returns_400():
    """An alias containing characters outside [A-Za-z0-9_-] returns 400."""
    r = client.post("/shorten", json={"url": "https://example.com", "alias": "bad alias!"})
    assert r.status_code == 400


def test_alias_too_long_returns_400():
    """An alias longer than 30 characters returns 400."""
    long_alias = "a" * 31
    r = client.post("/shorten", json={"url": "https://example.com", "alias": long_alias})
    assert r.status_code == 400


def test_no_alias_still_auto_generates():
    """Omitting alias keeps the original auto-generation behaviour."""
    r = client.post("/shorten", json={"url": "https://example.com"})
    assert r.status_code == 200
    data = r.json()
    assert data["code"]
    assert data["short_url"] == f"/{data['code']}"
