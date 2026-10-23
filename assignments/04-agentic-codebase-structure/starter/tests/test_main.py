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
    alias = f"my-alias-{uuid.uuid4().hex[:8]}"
    r = client.post(
        "/shorten",
        json={"url": "https://example.com/custom-target", "alias": alias},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["code"] == alias
    assert data["short_url"] == f"/{alias}"

    # Verify redirection
    r2 = client.get(f"/{alias}", follow_redirects=False)
    assert r2.status_code == 307
    assert r2.headers["location"] == "https://example.com/custom-target"


def test_custom_alias_conflict_409():
    alias = f"conflict-{uuid.uuid4().hex[:8]}"
    r1 = client.post(
        "/shorten",
        json={"url": "https://example.com/1", "alias": alias},
    )
    assert r1.status_code == 200

    # Second attempt with same alias must return 409
    r2 = client.post(
        "/shorten",
        json={"url": "https://example.com/2", "alias": alias},
    )
    assert r2.status_code == 409
    assert "taken" in r2.json()["detail"].lower()


def test_custom_alias_reserved_name_409():
    for reserved in ["docs", "redoc", "openapi.json", "shorten"]:
        r = client.post(
            "/shorten",
            json={"url": "https://example.com/reserved", "alias": reserved},
        )
        assert r.status_code == 409
        assert "reserved" in r.json()["detail"].lower()


def test_custom_alias_invalid_characters_400():
    invalid_aliases = [
        "with space",
        "bad/slash",
        "bad?query",
        "bad#hash",
        "bad@at",
        "a" * 33,  # too long (>32)
        "",        # empty string
    ]
    for bad_alias in invalid_aliases:
        r = client.post(
            "/shorten",
            json={"url": "https://example.com/bad", "alias": bad_alias},
        )
        assert r.status_code == 400


def test_auto_generated_code_avoids_alias_collision(tmp_path, monkeypatch):
    import main

    # Use isolated database
    test_db = tmp_path / "test_collision.db"
    monkeypatch.setattr(main, "DB_PATH", test_db)
    main.init_db()

    # encode(2) would normally be the code for row id 2
    colliding_code = main.encode(2)

    # First shorten creates row id 1 with custom alias equal to colliding_code
    r1 = client.post(
        "/shorten",
        json={"url": "https://example.com/alias-first", "alias": colliding_code},
    )
    assert r1.status_code == 200
    assert r1.json()["code"] == colliding_code

    # Second shorten without alias gets row id 2.
    # The application must detect the collision with colliding_code and pick an alternative code.
    r2 = client.post(
        "/shorten",
        json={"url": "https://example.com/auto-second"},
    )
    assert r2.status_code == 200
    auto_code = r2.json()["code"]
    assert auto_code != colliding_code

    # Verify both codes redirect correctly
    r3 = client.get(f"/{colliding_code}", follow_redirects=False)
    assert r3.status_code == 307
    assert r3.headers["location"] == "https://example.com/alias-first"

    r4 = client.get(f"/{auto_code}", follow_redirects=False)
    assert r4.status_code == 307
    assert r4.headers["location"] == "https://example.com/auto-second"
