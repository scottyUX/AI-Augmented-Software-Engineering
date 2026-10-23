"""Click counter: GET /stats/{code} -> {"url": ..., "clicks": N}."""


def visit(client, code):
    return client.get(f"/{code}", follow_redirects=False)


def test_new_link_has_zero_clicks(client, shorten):
    code = shorten("https://example.com/new")
    r = client.get(f"/stats/{code}")
    assert r.status_code == 200
    assert r.json() == {"url": "https://example.com/new", "clicks": 0}


def test_stats_counts_each_redirect(client, shorten):
    code = shorten()
    for _ in range(3):
        assert visit(client, code).status_code == 307
    assert client.get(f"/stats/{code}").json()["clicks"] == 3


def test_clicks_are_tracked_per_code(client, shorten):
    a = shorten("https://a.example")
    b = shorten("https://b.example")
    visit(client, a)
    visit(client, a)
    visit(client, b)
    assert client.get(f"/stats/{a}").json()["clicks"] == 2
    assert client.get(f"/stats/{b}").json()["clicks"] == 1


def test_viewing_stats_does_not_count_as_a_click(client, shorten):
    code = shorten()
    client.get(f"/stats/{code}")
    client.get(f"/stats/{code}")
    assert client.get(f"/stats/{code}").json()["clicks"] == 0


def test_stats_unknown_code_returns_404(client):
    r = client.get("/stats/nope")
    assert r.status_code == 404
    assert r.json()["detail"] == "unknown code"


def test_unknown_code_visit_is_404_and_counts_nothing(client, shorten):
    code = shorten()
    assert visit(client, "does-not-exist").status_code == 404
    assert client.get(f"/stats/{code}").json()["clicks"] == 0


def test_existing_database_without_clicks_column_is_migrated(tmp_path, monkeypatch):
    """A links.db created by the old schema keeps working after upgrade."""
    import sqlite3
    from fastapi.testclient import TestClient
    import main

    db = tmp_path / "old.db"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE links (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT UNIQUE, url TEXT NOT NULL)")
        conn.execute("INSERT INTO links (code, url) VALUES ('b', 'https://old.example')")
    monkeypatch.setattr(main, "DB_PATH", db)
    main.init_db()
    client = TestClient(main.app)

    assert client.get("/b", follow_redirects=False).status_code == 307
    assert client.get("/stats/b").json() == {"url": "https://old.example", "clicks": 1}
