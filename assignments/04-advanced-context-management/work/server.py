"""Data Explorer — MCP server for Week 4.

Exposes country data to an agent as two MCP tools over STDIO:

    search_countries(query, limit)  -> short list of matching countries
    get_country_details(name)       -> currencies, languages, borders, flag

Data source
-----------
The starter used the REST Countries v3.1 API (https://restcountries.com/v3.1). As of
October 2026 that version is deprecated: every request gets a 302 redirect to a JSON
error ("This API version has been deprecated."), and the new v5 API requires an API key.
To keep the server free and key-less, it now loads the open `mledoze/countries` dataset
(the same data REST Countries was built on) from GitHub once, caches it in memory, and
filters it locally. Flag images come from flagcdn.com.

Every failure (bad input, HTTP error, timeout, no results, bad JSON) is returned as a
clean, structured message instead of an exception, so the server never crashes.

Setup:
    pip install -r requirements.txt
Run (STDIO):
    python server.py
"""
import os

import httpx
from mcp.server.fastmcp import FastMCP

DATA_URL = os.environ.get(
    "COUNTRIES_DATA_URL",
    "https://raw.githubusercontent.com/mledoze/countries/master/countries.json",
)
FLAG_URL = "https://flagcdn.com/w320/{code}.png"
TIMEOUT_SECONDS = 10
MAX_QUERY_LENGTH = 100
MAX_LIMIT = 25

mcp = FastMCP("data-explorer")

_cache: list[dict] | None = None  # the dataset, loaded on first use


def _clean_text(value: str | None) -> str:
    """Return a stripped string, treating None as empty."""
    return (value or "").strip() if isinstance(value, str) else ""


def _validate_name(value: str | None, field: str) -> str | None:
    """Return an error message if the name is unusable, otherwise None."""
    if value is not None and not isinstance(value, str):
        return f"{field} must be text"
    text = _clean_text(value)
    if not text:
        return f"{field} must not be empty"
    if len(text) > MAX_QUERY_LENGTH:
        return f"{field} is too long (max {MAX_QUERY_LENGTH} characters)"
    return None


def _load_countries() -> tuple[list[dict] | None, str | None]:
    """Download the dataset once and return (countries, error).

    Timeouts, network errors, non-2xx responses and invalid JSON return (None, message).
    A failed download is not cached, so the next call tries again.
    """
    global _cache
    if _cache is not None:
        return _cache, None
    try:
        resp = httpx.get(DATA_URL, timeout=TIMEOUT_SECONDS, follow_redirects=True)
    except httpx.TimeoutException:
        return None, f"the country data source did not respond within {TIMEOUT_SECONDS} seconds"
    except httpx.HTTPError as exc:
        return None, f"could not reach the country data source: {exc.__class__.__name__}"

    if resp.status_code >= 400:
        return None, f"the country data source returned HTTP {resp.status_code}"
    try:
        data = resp.json()
    except ValueError:
        return None, "the country data source returned a response that is not valid JSON"
    if not isinstance(data, list) or not data:
        return None, "unexpected response format from the country data source"

    _cache = data
    return _cache, None


def _names(country: dict) -> list[str]:
    """All lower-cased names a country can be found by (common, official, alt spellings)."""
    name = country.get("name") or {}
    candidates = [name.get("common"), name.get("official"), *(country.get("altSpellings") or [])]
    return [c.lower() for c in candidates if isinstance(c, str)]


def _match(countries: list[dict], query: str) -> list[dict]:
    """Exact name matches first, then partial matches, without duplicates."""
    q = query.lower()
    exact = [c for c in countries if q in _names(c)]
    partial = [c for c in countries if c not in exact and any(q in n for n in _names(c))]
    return exact + partial


@mcp.tool()
def search_countries(query: str, limit: int = 5) -> list[dict]:
    """Search countries by (part of) their name.

    Args:
        query: Full or partial country name, e.g. "united" or "Turkey".
        limit: Maximum number of results to return (1-25, default 5).

    Returns a list of {name, capital, region, subregion}. An empty list means no
    country matched. On failure, returns a single item: [{"error": "..."}].
    """
    error = _validate_name(query, "query")
    if error:
        return [{"error": error}]
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_LIMIT:
        return [{"error": f"limit must be an integer between 1 and {MAX_LIMIT}"}]

    countries, error = _load_countries()
    if error:
        return [{"error": error}]

    results = []
    for c in _match(countries, _clean_text(query))[:limit]:
        results.append(
            {
                "name": (c.get("name") or {}).get("common"),
                "capital": (c.get("capital") or [None])[0],
                "region": c.get("region"),
                "subregion": c.get("subregion"),
            }
        )
    return results


@mcp.tool()
def get_country_details(name: str) -> dict:
    """Get details for one country: currencies, languages, borders and flag.

    Args:
        name: The country's name, e.g. "Japan" or "Türkiye". An exact name match is
              preferred ("Niger" will not return "Nigeria"); otherwise the first
              partial match is used.

    Returns {name, official_name, currencies, languages, borders, flag_url, flag_emoji}.
    `currencies` is a list of {code, name, symbol}; `borders` is a list of neighbouring
    country names (empty for island nations). On failure or no match, returns
    {"error": "..."}.
    """
    error = _validate_name(name, "name")
    if error:
        return {"error": error}

    countries, error = _load_countries()
    if error:
        return {"error": error}

    clean = _clean_text(name)
    matches = _match(countries, clean)
    if not matches:
        return {"error": f"no country found matching '{clean}'"}

    c = matches[0]
    by_code = {x.get("cca3"): (x.get("name") or {}).get("common") for x in countries}
    currencies = [
        {"code": code, "name": info.get("name"), "symbol": info.get("symbol")}
        for code, info in (c.get("currencies") or {}).items()
    ]
    cca2 = _clean_text(c.get("cca2")).lower()
    return {
        "name": (c.get("name") or {}).get("common"),
        "official_name": (c.get("name") or {}).get("official"),
        "currencies": currencies,
        "languages": sorted((c.get("languages") or {}).values()),
        "borders": [by_code.get(code) or code for code in (c.get("borders") or [])],
        "flag_url": FLAG_URL.format(code=cca2) if cca2 else None,
        "flag_emoji": c.get("flag"),
    }


if __name__ == "__main__":
    mcp.run()
