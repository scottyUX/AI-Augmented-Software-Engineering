"""Offline tests for server.py — HTTP is faked with monkeypatch, no network needed.

Run:  pytest -q
"""
import httpx
import pytest

import server

# ---------------------------------------------------------------- fake payloads
V5_JORDAN = {
    "names": {"common": "Jordan", "official": "Hashemite Kingdom of Jordan", "alternates": ["JO"]},
    "capitals": [{"name": "Amman", "attributes": {"primary": True}}],
    "region": "Asia",
    "population": 11_000_000,
    "currencies": [{"code": "JOD", "name": "Jordanian dinar", "symbol": "د.ا"}],
    "languages": [{"name": "Arabic", "bcp47": "ar"}],
    "borders": ["IRQ", "ISR", "PSE", "SAU", "SYR"],
    "flag": {"emoji": "🇯🇴", "url_png": "https://flags.restcountries.com/v5/w640/jo.png"},
}
V5_NIGERIA = {"names": {"common": "Nigeria", "official": "Federal Republic of Nigeria"}}
V5_NIGER = {"names": {"common": "Niger", "official": "Republic of Niger"},
            "capitals": [{"name": "Niamey"}]}


def v5_body(*objects):
    return {"data": {"objects": list(objects), "meta": {"total": len(objects)}}}


OPEN_DATA = [
    {"name": {"common": "Jordan", "official": "Hashemite Kingdom of Jordan"}, "cca2": "JO",
     "capital": ["Amman"], "region": "Asia", "altSpellings": ["JO"],
     "currencies": {"JOD": {"name": "Jordanian dinar", "symbol": "د.ا"}},
     "languages": {"ara": "Arabic"}, "borders": ["IRQ", "ISR", "PSE", "SAU", "SYR"], "flag": "🇯🇴"},
    {"name": {"common": "Nigeria", "official": "Federal Republic of Nigeria"}, "cca2": "NG"},
    {"name": {"common": "Niger", "official": "Republic of Niger"}, "cca2": "NE", "capital": ["Niamey"]},
    {"name": {"common": "Antarctica", "official": "Antarctica"}},
]


# ---------------------------------------------------------------- fake http
def resp(status, json=None, text=None):
    req = httpx.Request("GET", "https://example.test")
    if json is not None:
        return httpx.Response(status, json=json, request=req)
    return httpx.Response(status, text=text or "", request=req)


def fake_get(*responses):
    """A fake httpx.get that replays responses (Response objects or exceptions) and records calls."""
    queue, calls = list(responses), []

    def _get(url, params=None, headers=None, timeout=None):
        calls.append({"url": url, "params": params, "headers": headers})
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    _get.calls = calls
    return _get


@pytest.fixture(autouse=True)
def fresh_state(monkeypatch):
    monkeypatch.setattr(server, "_open_data_cache", None)
    monkeypatch.delenv("RESTCOUNTRIES_API_KEY", raising=False)


@pytest.fixture
def v5(monkeypatch):
    monkeypatch.setenv("RESTCOUNTRIES_API_KEY", "test-key")


# ============================================================ v5 API (key set)
def test_v5_details_shape(v5, monkeypatch):
    get = fake_get(resp(200, v5_body(V5_JORDAN)))
    monkeypatch.setattr(server.httpx, "get", get)
    assert server.get_country_details("Jordan") == {
        "name": "Jordan",
        "official_name": "Hashemite Kingdom of Jordan",
        "capital": "Amman",
        "region": "Asia",
        "currencies": [{"code": "JOD", "name": "Jordanian dinar", "symbol": "د.ا"}],
        "languages": ["Arabic"],
        "borders": ["IRQ", "ISR", "PSE", "SAU", "SYR"],
        "flag_url": "https://flags.restcountries.com/v5/w640/jo.png",
        "flag_emoji": "🇯🇴",
        "source": "restcountries-v5",
    }
    assert get.calls[0]["url"] == server.V5_URL
    assert get.calls[0]["params"] == {"q": "Jordan"}
    assert get.calls[0]["headers"] == {"Authorization": "Bearer test-key"}


def test_v5_exact_name_beats_partial(v5, monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(200, v5_body(V5_NIGERIA, V5_NIGER))))
    out = server.get_country_details("niger")
    assert out["name"] == "Niger" and out["other_matches"] == ["Nigeria"]


def test_v5_search_success(v5, monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(200, v5_body(V5_JORDAN))))
    assert server.search_countries("jordan") == [
        {"name": "Jordan", "capital": "Amman", "region": "Asia", "population": 11_000_000}
    ]


def test_v5_empty_result(v5, monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(200, v5_body())))
    assert server.search_countries("atlantis") == []


def test_v5_404_is_not_found(v5, monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(404, {"errors": []})))
    assert server.get_country_details("Atlantis")["error_type"] == "not_found"


@pytest.mark.parametrize("status", [401, 403])
def test_v5_bad_key(v5, monkeypatch, status):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(status, {"errors": []})))
    assert server.get_country_details("Jordan")["error_type"] == "auth"


def test_v5_rate_limited(v5, monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(429, text="slow down")))
    assert server.search_countries("jordan")[0]["error_type"] == "rate_limited"


def test_v5_unexpected_shape(v5, monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(200, {"success": False, "data": None})))
    assert server.get_country_details("Jordan")["error_type"] == "bad_response"


def test_v5_missing_fields_do_not_crash(v5, monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(200, v5_body({"names": {"common": "X"}}))))
    out = server.get_country_details("X")
    assert out["currencies"] == [] and out["languages"] == [] and out["borders"] == []
    assert out["capital"] is None and out["flag_url"] is None


# ======================================================= open dataset (no key)
def test_open_data_details_shape(monkeypatch):
    get = fake_get(resp(200, OPEN_DATA))
    monkeypatch.setattr(server.httpx, "get", get)
    out = server.get_country_details("Jordan")
    assert out["name"] == "Jordan" and out["capital"] == "Amman"
    assert out["currencies"] == [{"code": "JOD", "name": "Jordanian dinar", "symbol": "د.ا"}]
    assert out["languages"] == ["Arabic"]
    assert out["flag_url"] == "https://flagcdn.com/w320/jo.png"
    assert get.calls[0]["url"] == server.OPEN_DATA_URL


def test_open_data_is_downloaded_once(monkeypatch):
    get = fake_get(resp(200, OPEN_DATA))
    monkeypatch.setattr(server.httpx, "get", get)
    server.search_countries("jordan")
    server.get_country_details("Niger")
    assert len(get.calls) == 1


def test_open_data_ranks_exact_match_first(monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(200, OPEN_DATA)))
    assert [c["name"] for c in server.search_countries("niger")] == ["Niger", "Nigeria"]


def test_open_data_no_match(monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(200, OPEN_DATA)))
    assert server.search_countries("atlantis") == []
    assert server.get_country_details("Atlantis")["error_type"] == "not_found"


def test_open_data_failed_download_is_retried(monkeypatch):
    get = fake_get(httpx.ConnectError("dns"), resp(200, OPEN_DATA))
    monkeypatch.setattr(server.httpx, "get", get)
    assert server.get_country_details("Jordan")["error_type"] == "network"
    assert server.get_country_details("Jordan")["name"] == "Jordan"


# ================================================================ input + transport
@pytest.mark.parametrize("bad", ["", "   ", "123", "drop table;", "x" * 101, None, "<script>"])
def test_rejects_bad_names_without_network(monkeypatch, bad):
    get = fake_get()
    monkeypatch.setattr(server.httpx, "get", get)
    assert server.search_countries(bad)[0]["error_type"] == "invalid_input"
    assert server.get_country_details(bad)["error_type"] == "invalid_input"
    assert get.calls == []


@pytest.mark.parametrize("ok", ["Côte d'Ivoire", "Guinea-Bissau", "St. Lucia", "Congo (Kinshasa)", "الأردن"])
def test_accepts_real_country_names(monkeypatch, ok):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(200, OPEN_DATA)))
    assert isinstance(server.search_countries(ok), list)


@pytest.mark.parametrize("bad_limit", [0, -1, 26, "5", True])
def test_rejects_bad_limit(bad_limit):
    assert server.search_countries("jordan", limit=bad_limit)[0]["error_type"] == "invalid_input"


def test_respects_limit(monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(200, OPEN_DATA)))
    assert len(server.search_countries("i", limit=2)) == 2


@pytest.mark.parametrize("exc, kind", [
    (httpx.ReadTimeout("slow"), "timeout"),
    (httpx.ConnectTimeout("slow"), "timeout"),
    (httpx.ConnectError("dns"), "network"),
])
def test_transport_errors(v5, monkeypatch, exc, kind):
    monkeypatch.setattr(server.httpx, "get", fake_get(exc))
    assert server.get_country_details("Jordan")["error_type"] == kind


def test_http_500(v5, monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(500, text="boom")))
    out = server.search_countries("jordan")[0]
    assert out["error_type"] == "upstream_http" and "500" in out["error"]


def test_non_json_body(v5, monkeypatch):
    monkeypatch.setattr(server.httpx, "get", fake_get(resp(200, text="<html>")))
    assert server.get_country_details("Jordan")["error_type"] == "bad_response"
