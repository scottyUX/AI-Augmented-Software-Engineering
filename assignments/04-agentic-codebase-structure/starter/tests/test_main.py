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
    r = client.post("/shorten", json={"url": "https://example.com/test-custom", "alias": alias})
    assert r.status_code == 200
    data = r.json()
    assert data["code"] == alias
    assert data["short_url"] == f"/{alias}"

    # Verify redirection works
    r_redir = client.get(f"/{alias}", follow_redirects=False)
    assert r_redir.status_code == 307
    assert r_redir.headers["location"] == "https://example.com/test-custom"


def test_custom_alias_conflict_409():
    alias = f"conflict-{uuid.uuid4().hex[:8]}"
    r1 = client.post("/shorten", json={"url": "https://example.com/1", "alias": alias})
    assert r1.status_code == 200

    r2 = client.post("/shorten", json={"url": "https://example.com/2", "alias": alias})
    assert r2.status_code == 409


def test_custom_alias_reserved_name_409():
    for reserved in ["docs", "redoc", "openapi.json", "shorten"]:
        r = client.post("/shorten", json={"url": "https://example.com/reserved", "alias": reserved})
        assert r.status_code == 409


def test_custom_alias_invalid_characters_400():
    for bad_alias in ["with space", "bad/slash", "bad?query", "bad#hash", "a" * 33, ""]:
        r = client.post("/shorten", json={"url": "https://example.com/bad", "alias": bad_alias})
        assert r.status_code == 400


def test_auto_generated_code_avoids_alias_collision(tmp_path, monkeypatch):
    import main

    # Use an isolated temp database for this test to control IDs reliably
    test_db = tmp_path / "test_collision.db"
    monkeypatch.setattr(main, "DB_PATH", test_db)
    main.init_db()

    # encode(2) would be the code generated for row id 2
    colliding_code = main.encode(2)

    # First shorten creates row id 1 with custom alias equal to colliding_code
    r1 = client.post("/shorten", json={"url": "https://example.com/alias-first", "alias": colliding_code})
    assert r1.status_code == 200
    assert r1.json()["code"] == colliding_code

    # Second shorten without alias gets row id 2, whose standard encode is colliding_code.
    # The app must detect the collision and pick an alternative code without failing with 500.
    r2 = client.post("/shorten", json={"url": "https://example.com/auto-second"})
    assert r2.status_code == 200
    auto_code = r2.json()["code"]
    assert auto_code != colliding_code

    # Verify both redirect correctly
    r3 = client.get(f"/{colliding_code}", follow_redirects=False)
    assert r3.status_code == 307
    assert r3.headers["location"] == "https://example.com/alias-first"

    r4 = client.get(f"/{auto_code}", follow_redirects=False)
    assert r4.status_code == 307
    assert r4.headers["location"] == "https://example.com/auto-second"
