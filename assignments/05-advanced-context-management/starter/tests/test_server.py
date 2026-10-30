"""Test suite for Week 5 Data Explorer MCP server."""
import pytest
import httpx
from unittest.mock import patch, MagicMock

import server
from server import (
    search_countries,
    get_country_details,
    find_country,
    normalize_text,
    load_countries,
    mcp,
    FLAG_URL,
)

SAMPLE_COUNTRIES = [
    {
        "name": {
            "common": "Germany",
            "official": "Federal Republic of Germany",
        },
        "cca2": "DE",
        "cca3": "DEU",
        "cioc": "GER",
        "capital": ["Berlin"],
        "region": "Europe",
        "subregion": "Western Europe",
        "currencies": {
            "EUR": {"name": "Euro", "symbol": "€"}
        },
        "languages": {
            "deu": "German"
        },
        "borders": ["AUT", "BEL", "CZE", "DNK", "FRA", "LUX", "NLD", "POL", "CHE"],
        "altSpellings": ["DE", "Federal Republic of Germany", "Deutschland"],
    },
    {
        "name": {
            "common": "Türkiye",
            "official": "Republic of Turkey",
        },
        "cca2": "TR",
        "cca3": "TUR",
        "cioc": "TUR",
        "capital": ["Ankara"],
        "region": "Asia",
        "subregion": "Western Asia",
        "currencies": {
            "TRY": {"name": "Turkish lira", "symbol": "₺"}
        },
        "languages": {
            "tur": "Turkish"
        },
        "borders": ["ARM", "AZE", "BGR", "GEO", "GRC", "IRN", "IRQ", "SYR"],
        "altSpellings": ["TR", "Turkiye", "Republic of Turkey", "Türkiye Cumhuriyeti"],
    },
    {
        "name": {
            "common": "Dominica",
            "official": "Commonwealth of Dominica",
        },
        "cca2": "DM",
        "cca3": "DMA",
        "capital": ["Roseau"],
        "region": "Americas",
        "subregion": "Caribbean",
        "currencies": {
            "XCD": {"name": "Eastern Caribbean dollar", "symbol": "$"}
        },
        "languages": {
            "eng": "English"
        },
        "borders": [],
        "altSpellings": ["DM", "Dominique", "Commonwealth of Dominica"],
    },
    {
        "name": {
            "common": "Dominican Republic",
            "official": "Dominican Republic",
        },
        "cca2": "DO",
        "cca3": "DOM",
        "capital": ["Santo Domingo"],
        "region": "Americas",
        "subregion": "Caribbean",
        "currencies": {
            "DOP": {"name": "Dominican peso", "symbol": "$"}
        },
        "languages": {
            "spa": "Spanish"
        },
        "borders": ["HTI"],
        "altSpellings": ["DO"],
    },
    {
        "name": {
            "common": "United Kingdom",
            "official": "United Kingdom of Great Britain and Northern Ireland",
        },
        "cca2": "GB",
        "cca3": "GBR",
        "cioc": "GBR",
        "capital": ["London"],
        "region": "Europe",
        "subregion": "Northern Europe",
        "currencies": {
            "GBP": {"name": "British pound", "symbol": "£"}
        },
        "languages": {
            "eng": "English"
        },
        "borders": ["IRL"],
        "altSpellings": ["GB", "UK", "Great Britain"],
    },
]


@pytest.fixture(autouse=True)
def mock_dataset():
    """Mock the in-memory countries dataset for all tests to be deterministic and offline."""
    server._countries = SAMPLE_COUNTRIES
    yield
    server._countries = None


# ---------------------------------------------------------
# Tool Registration Tests
# ---------------------------------------------------------

def test_mcp_tools_registered():
    """Verify both required tools are registered on the FastMCP instance."""
    tools = mcp._tool_manager.list_tools()
    tool_names = [t.name for t in tools]
    assert "search_countries" in tool_names
    assert "get_country_details" in tool_names


# ---------------------------------------------------------
# Helper Function Tests
# ---------------------------------------------------------

def test_normalize_text():
    assert normalize_text("Türkiye") == "turkiye"
    assert normalize_text("  GERMANY  ") == "germany"
    assert normalize_text("") == ""
    assert normalize_text(None) == ""


def test_find_country_exact():
    c, candidates = find_country("Germany", SAMPLE_COUNTRIES)
    assert c is not None
    assert c["name"]["common"] == "Germany"
    assert candidates == []

    # Case & accent insensitive
    c2, _ = find_country("turkiye", SAMPLE_COUNTRIES)
    assert c2 is not None
    assert c2["cca3"] == "TUR"

    # Alt spelling & codes
    c3, _ = find_country("Turkey", SAMPLE_COUNTRIES)
    assert c3 is not None
    assert c3["cca3"] == "TUR"

    c4, _ = find_country("DEU", SAMPLE_COUNTRIES)
    assert c4 is not None
    assert c4["name"]["common"] == "Germany"

    c5, _ = find_country("UK", SAMPLE_COUNTRIES)
    assert c5 is not None
    assert c5["name"]["common"] == "United Kingdom"


def test_find_country_ambiguous():
    # "Dominic" matches both Dominica and Dominican Republic
    c, candidates = find_country("Dominic", SAMPLE_COUNTRIES)
    assert c is None
    assert "Dominica" in candidates
    assert "Dominican Republic" in candidates


def test_find_country_not_found():
    c, candidates = find_country("Atlantis", SAMPLE_COUNTRIES)
    assert c is None
    assert candidates == []


# ---------------------------------------------------------
# Tool 1: search_countries Tests
# ---------------------------------------------------------

def test_search_countries_success():
    results = search_countries("germany")
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["name"] == "Germany"
    assert results[0]["capital"] == "Berlin"
    assert results[0]["region"] == "Europe"
    assert results[0]["subregion"] == "Western Europe"


def test_search_countries_limit():
    results = search_countries("Dominic", limit=1)
    assert len(results) == 1


def test_search_countries_limit_clamping():
    results = search_countries("Dominic", limit=100)
    assert len(results) == 2


def test_search_countries_no_match():
    results = search_countries("Narnia")
    assert results == []


def test_search_countries_empty_input():
    res1 = search_countries("")
    assert "error" in res1[0]
    assert "non-empty" in res1[0]["error"]

    res2 = search_countries("   ")
    assert "error" in res2[0]


def test_search_countries_non_string_input():
    res = search_countries(None)
    assert "error" in res[0]
    assert "non-empty string" in res[0]["error"]

    res2 = search_countries(12345)
    assert "error" in res2[0]


def test_search_countries_invalid_limit():
    res = search_countries("germany", limit=0)
    assert "error" in res[0]
    assert "positive integer" in res[0]["error"]

    res2 = search_countries("germany", limit="five")
    assert "error" in res2[0]


# ---------------------------------------------------------
# Tool 2: get_country_details Tests
# ---------------------------------------------------------

def test_get_country_details_success():
    details = get_country_details("Germany")
    assert isinstance(details, dict)
    assert details["name"] == "Germany"
    assert details["official_name"] == "Federal Republic of Germany"
    assert details["cca2"] == "DE"
    assert details["cca3"] == "DEU"
    assert "EUR" in details["currencies"]
    assert details["currencies"]["EUR"]["name"] == "Euro"
    assert "deu" in details["languages"]
    assert "AUT" in details["borders"]
    assert details["flag_url"] == FLAG_URL.format(cca3="deu")
    assert details["flag_url"].endswith("/deu.svg")


def test_get_country_details_turkish_spelling():
    # Search by common Turkish name
    details = get_country_details("Turkey")
    assert details["name"] == "Türkiye"
    assert details["cca3"] == "TUR"
    assert "TRY" in details["currencies"]
    assert details["flag_url"].endswith("/tur.svg")


def test_get_country_details_empty_input():
    res1 = get_country_details("")
    assert "error" in res1
    assert "non-empty" in res1["error"]

    res2 = get_country_details("   ")
    assert "error" in res2


def test_get_country_details_non_string_input():
    res = get_country_details(None)
    assert "error" in res
    assert "non-empty string" in res["error"]

    res2 = get_country_details(999)
    assert "error" in res2


def test_get_country_details_not_found():
    res = get_country_details("Wakanda")
    assert "error" in res
    assert "not found" in res["error"]


def test_get_country_details_ambiguous():
    res = get_country_details("Dominic")
    assert "error" in res
    assert "ambiguous" in res["error"]
    assert "candidates" in res
    assert len(res["candidates"]) == 2


# ---------------------------------------------------------
# Robust Error Handling & Upstream Failure Tests
# ---------------------------------------------------------

def test_upstream_timeout_handling():
    server._countries = None
    with patch("httpx.get", side_effect=httpx.TimeoutException("Connection timed out")):
        res_search = search_countries("germany")
        assert "error" in res_search[0]
        assert "timed out" in res_search[0]["error"]
        assert res_search[0].get("retryable") is True

        res_details = get_country_details("germany")
        assert "error" in res_details
        assert "timed out" in res_details["error"]
        assert res_details.get("retryable") is True


def test_upstream_http_error_handling():
    server._countries = None
    mock_resp = MagicMock()
    mock_resp.status_code = 503
    with patch("httpx.get", side_effect=httpx.HTTPStatusError("503 Service Unavailable", request=MagicMock(), response=mock_resp)):
        res_search = search_countries("germany")
        assert "error" in res_search[0]
        assert "upstream request failed" in res_search[0]["error"]
        assert res_search[0].get("retryable") is True

        res_details = get_country_details("germany")
        assert "error" in res_details
        assert "upstream request failed" in res_details["error"]
        assert res_details.get("retryable") is True


def test_upstream_malformed_json_handling():
    server._countries = None
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"error": "not a list"}
    mock_resp.raise_for_status.return_value = None
    with patch("httpx.get", return_value=mock_resp):
        res = search_countries("germany")
        assert "error" in res[0]
        assert "failed to load country dataset" in res[0]["error"]


def test_upstream_recovery_after_failure():
    """Verify that a failure is not cached, allowing subsequent calls to recover."""
    server._countries = None
    # 1. First call fails with timeout
    with patch("httpx.get", side_effect=httpx.TimeoutException("Timeout")):
        res_fail = search_countries("germany")
        assert "timed out" in res_fail[0]["error"]
        assert server._countries is None

    # 2. Next call succeeds
    mock_resp = MagicMock()
    mock_resp.json.return_value = SAMPLE_COUNTRIES
    mock_resp.raise_for_status.return_value = None
    with patch("httpx.get", return_value=mock_resp):
        res_success = search_countries("germany")
        assert len(res_success) == 1
        assert res_success[0]["name"] == "Germany"
        assert server._countries == SAMPLE_COUNTRIES
