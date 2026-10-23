"""Data Explorer — an MCP server that gives an agent country data.

Exposes two tools over STDIO:

* ``search_countries(query, limit)``  – find countries by (partial) name.
* ``get_country_details(name)``       – currencies, languages, borders and flag for one country.

Data source
-----------
REST Countries retired its free, no-key ``/v3.1`` API: every v3.1 URL now redirects to a
"This API version has been deprecated" message. The current API (``/countries/v5``) needs
a free key, so the server picks a source at runtime:

* ``RESTCOUNTRIES_API_KEY`` is set  -> REST Countries v5 (``api.restcountries.com``).
* no key                            -> the open ``mledoze/countries`` dataset (the data
  REST Countries was originally built on), downloaded once and searched locally.

Both sources are mapped to the same output shape, so the agent never sees the difference
(except ``source`` and a ``population`` of ``null`` in the no-key dataset).

Both tools never raise: every failure (bad input, missing key, HTTP error, timeout, bad
JSON, no results) comes back as a small structured value the model can read and act on.

Setup:   pip install -r requirements.txt
Run:     python server.py            # register this command in your MCP client
"""
from __future__ import annotations

import os
import re
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

V5_URL = "https://api.restcountries.com/countries/v5"
OPEN_DATA_URL = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"
TIMEOUT_SECONDS = 10.0
MAX_NAME_LENGTH = 100
MAX_LIMIT = 25

# Letters (any script), spaces, and the punctuation that appears in real country
# names: "Côte d'Ivoire", "Guinea-Bissau", "St. Lucia", "Congo (Kinshasa)".
_VALID_NAME = re.compile(r"^[^\W\d_]+(?:[\s'’.\-(),&][^\W\d_]*)*$", re.UNICODE)

mcp = FastMCP("data-explorer")
_open_data_cache: list[dict] | None = None


# =========================================================================== helpers
def _error(message: str, kind: str) -> dict[str, str]:
    """Uniform error shape: the model always sees ``{"error": ..., "error_type": ...}``."""
    return {"error": message, "error_type": kind}


def _validate_name(value: Any, field: str) -> tuple[str | None, dict | None]:
    """Return (clean_value, None) or (None, error_dict)."""
    if not isinstance(value, str):
        return None, _error(f"{field} must be a string", "invalid_input")
    cleaned = " ".join(value.split())  # trim + collapse internal whitespace
    if not cleaned:
        return None, _error(f"{field} must not be empty", "invalid_input")
    if len(cleaned) > MAX_NAME_LENGTH:
        return None, _error(f"{field} is too long (max {MAX_NAME_LENGTH} characters)", "invalid_input")
    if not _VALID_NAME.match(cleaned):
        return None, _error(f"{field} may only contain letters, spaces and . ' - ( ) , &", "invalid_input")
    return cleaned, None


def _http_get_json(url: str, params: dict | None = None, headers: dict | None = None):
    """GET a URL and decode JSON. Returns ``(status, data, None)`` or ``(None, None, error)``."""
    try:
        resp = httpx.get(url, params=params, headers=headers, timeout=TIMEOUT_SECONDS)
    except httpx.TimeoutException:
        return None, None, _error(
            f"the country API did not respond within {TIMEOUT_SECONDS:g}s; try again later", "timeout"
        )
    except httpx.RequestError as exc:
        return None, None, _error(f"could not reach the country API: {exc.__class__.__name__}", "network")

    if resp.status_code in (401, 403):
        return None, None, _error(
            "REST Countries rejected the API key (HTTP %d); check RESTCOUNTRIES_API_KEY" % resp.status_code,
            "auth",
        )
    if resp.status_code == 429:
        return None, None, _error("rate limited by REST Countries (HTTP 429); wait and retry", "rate_limited")
    if resp.status_code == 404:
        return 404, None, None
    if resp.status_code >= 400:
        return None, None, _error(f"the country API returned HTTP {resp.status_code}", "upstream_http")
    try:
        return resp.status_code, resp.json(), None
    except ValueError:
        return None, None, _error("the country API returned a response that is not JSON", "bad_response")


# ------------------------------------------------------------------ source: v5 API
def _search_v5(query: str, key: str) -> tuple[list[dict] | None, dict | None]:
    status, data, err = _http_get_json(V5_URL, params={"q": query}, headers={"Authorization": f"Bearer {key}"})
    if err:
        return None, err
    if status == 404:
        return [], None
    payload = data.get("data") if isinstance(data, dict) else None
    objects = payload.get("objects") if isinstance(payload, dict) else None
    if not isinstance(objects, list):
        return None, _error("REST Countries returned an unexpected response shape", "bad_response")
    return [_from_v5(c) for c in objects if isinstance(c, dict)], None


def _from_v5(c: dict) -> dict:
    names = c.get("names") or {}
    capitals = c.get("capitals") or []
    primary = next((cap for cap in capitals if (cap.get("attributes") or {}).get("primary")), None)
    flag = c.get("flag") or {}
    return {
        "name": names.get("common"),
        "official_name": names.get("official"),
        "alt_names": list(names.get("alternates") or []),
        "capital": (primary or (capitals[0] if capitals else {})).get("name"),
        "region": c.get("region"),
        "population": c.get("population"),
        "currencies": [
            {"code": cur.get("code"), "name": cur.get("name"), "symbol": cur.get("symbol")}
            for cur in (c.get("currencies") or [])
        ],
        "languages": [lang.get("name") for lang in (c.get("languages") or []) if lang.get("name")],
        "borders": list(c.get("borders") or []),
        "flag_url": flag.get("url_png") or flag.get("url_svg"),
        "flag_emoji": flag.get("emoji"),
        "source": "restcountries-v5",
    }


# ------------------------------------------------------------- source: open dataset
def _load_open_data() -> tuple[list[dict] | None, dict | None]:
    global _open_data_cache
    if _open_data_cache is None:
        _, data, err = _http_get_json(OPEN_DATA_URL)
        if err:
            return None, err
        if not isinstance(data, list):
            return None, _error("the country dataset has an unexpected shape", "bad_response")
        _open_data_cache = [_from_open_data(c) for c in data if isinstance(c, dict)]
    return _open_data_cache, None


def _from_open_data(c: dict) -> dict:
    names = c.get("name") or {}
    cca2 = str(c.get("cca2") or "").lower()
    return {
        "name": names.get("common"),
        "official_name": names.get("official"),
        "alt_names": list(c.get("altSpellings") or []),
        "capital": (c.get("capital") or [None])[0],
        "region": c.get("region"),
        "population": None,  # not included in this dataset
        "currencies": [
            {"code": code, "name": (info or {}).get("name"), "symbol": (info or {}).get("symbol")}
            for code, info in sorted((c.get("currencies") or {}).items())
        ],
        "languages": sorted((c.get("languages") or {}).values()),
        "borders": list(c.get("borders") or []),
        "flag_url": f"https://flagcdn.com/w320/{cca2}.png" if cca2 else None,
        "flag_emoji": c.get("flag"),
        "source": "mledoze/countries (no API key set)",
    }


def _search_open_data(query: str) -> tuple[list[dict] | None, dict | None]:
    countries, err = _load_open_data()
    if err:
        return None, err
    q = query.casefold()
    return [
        c for c in countries
        if any(q in str(n).casefold() for n in [c["name"], c["official_name"], *c["alt_names"]] if n)
    ], None


# ---------------------------------------------------------------------- dispatch
def _search(query: str) -> tuple[list[dict] | None, dict | None]:
    key = os.environ.get("RESTCOUNTRIES_API_KEY", "").strip()
    return _search_v5(query, key) if key else _search_open_data(query)


def _rank(countries: list[dict], wanted: str) -> list[dict]:
    """Exact common/official name first, then exact alternate name, then names starting with
    the query, then everything else (stable)."""
    w = wanted.casefold()

    def score(c: dict) -> int:
        main = {str(c.get("name") or "").casefold(), str(c.get("official_name") or "").casefold()}
        if w in main:
            return 0
        if w in {str(a).casefold() for a in c.get("alt_names", [])}:
            return 1
        if str(c.get("name") or "").casefold().startswith(w):
            return 2
        return 3

    return sorted(countries, key=score)


# ============================================================================ tools
@mcp.tool()
def search_countries(query: str, limit: int = 5) -> list[dict]:
    """Search countries by (partial) name.

    Returns up to ``limit`` items shaped ``{name, capital, region, population}``,
    best matches first. An empty list means no country matched. On failure returns a
    one-item list ``[{"error": ..., "error_type": ...}]``.
    """
    clean, err = _validate_name(query, "query")
    if err:
        return [err]
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_LIMIT:
        return [_error(f"limit must be an integer between 1 and {MAX_LIMIT}", "invalid_input")]

    found, err = _search(clean)
    if err:
        return [err]
    return [
        {k: c.get(k) for k in ("name", "capital", "region", "population")}
        for c in _rank(found, clean)[:limit]
    ]  # [] when nothing matched: not an error


@mcp.tool()
def get_country_details(name: str) -> dict:
    """Get details for ONE country by its common or official name (e.g. "Jordan").

    Returns ``{name, official_name, capital, region, currencies, languages, borders,
    flag_url, flag_emoji, source}`` where ``currencies`` is a list of
    ``{code, name, symbol}``, ``languages`` a list of names and ``borders`` a list of
    ISO 3166-1 alpha-3 codes (empty for island nations). If the name is ambiguous the
    best match is returned and ``other_matches`` lists the rest.
    On failure or no match returns ``{"error": ..., "error_type": ...}``.
    Use ``search_countries`` first if you are unsure of the exact name.
    """
    clean, err = _validate_name(name, "name")
    if err:
        return err

    found, err = _search(clean)
    if err:
        return err
    if not found:
        return _error(
            f"no country found matching '{clean}'; try search_countries to find the exact name",
            "not_found",
        )

    best, *rest = _rank(found, clean)
    result = {
        k: best.get(k)
        for k in ("name", "official_name", "capital", "region", "currencies", "languages",
                  "borders", "flag_url", "flag_emoji", "source")
    }
    if rest:
        result["other_matches"] = [c["name"] for c in rest if c.get("name")][:5]
    return result


if __name__ == "__main__":
    mcp.run()  # STDIO transport by default
