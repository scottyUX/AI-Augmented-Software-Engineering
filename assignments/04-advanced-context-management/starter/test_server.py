"""Integration test suite for Data Explorer MCP Server.

Validates:
1. Normal operations: search_countries and get_country_details.
2. Error handling: empty strings, invalid country names, whitespace.
3. Model-friendly return shapes and types.
"""
import pytest
from server import search_countries, get_country_details


def test_search_countries_valid():
    results = search_countries("turkey")
    assert isinstance(results, list)
    assert len(results) >= 1
    item = results[0]
    assert "name" in item
    assert "capital" in item
    assert "region" in item
    assert "population" in item


def test_search_countries_limit():
    results = search_countries("a", limit=2)
    assert isinstance(results, list)
    assert len(results) <= 2


def test_search_countries_empty_input():
    results = search_countries("   ")
    assert isinstance(results, list)
    assert len(results) == 1
    assert "error" in results[0]
    assert "empty" in results[0]["error"].lower()


def test_search_countries_not_found():
    results = search_countries("xyznonexistentcountry123")
    assert isinstance(results, list)
    assert len(results) == 0


def test_get_country_details_valid():
    details = get_country_details("Germany")
    assert isinstance(details, dict)
    assert "error" not in details
    assert details["name"] == "Germany"
    assert "official_name" in details
    assert isinstance(details["currencies"], list)
    assert len(details["currencies"]) >= 1
    assert details["currencies"][0]["code"] == "EUR"
    assert "German" in details["languages"]
    assert "FRA" in details["borders"]
    assert details["flag_url"] is not None
    assert details["flag_url"].startswith("http")


def test_get_country_details_empty_input():
    details = get_country_details("")
    assert isinstance(details, dict)
    assert "error" in details
    assert "empty" in details["error"].lower()


def test_get_country_details_not_found():
    details = get_country_details("xyznonexistentcountry123")
    assert isinstance(details, dict)
    assert "error" in details
    assert "No country found" in details["error"]
