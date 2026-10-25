"""Data Explorer — MCP server for Week 4.

Wraps country data (REST Countries schema) and exposes it to an agent
as MCP tools over STDIO with robust error handling and model-friendly return shapes.

Supported tools:
  - search_countries(query, limit): search countries by name / partial match.
  - get_country_details(name): returns currencies, languages, borders, and flag URL.

Setup:
    pip install -r requirements.txt
Run (STDIO):
    python server.py
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://restcountries.com/v3.1"
DATA_FILE = Path(__file__).parent / "countries.json"

mcp = FastMCP("data-explorer")

# In-memory country cache loaded from bundled snapshot
_COUNTRIES_CACHE: Optional[List[Dict[str, Any]]] = None


def _load_local_countries() -> List[Dict[str, Any]]:
    global _COUNTRIES_CACHE
    if _COUNTRIES_CACHE is None:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                _COUNTRIES_CACHE = json.load(f)
        else:
            _COUNTRIES_CACHE = []
    return _COUNTRIES_CACHE


def _get_flag_url(country: Dict[str, Any]) -> Optional[str]:
    """Helper to extract flag URL, fallback to flagcdn using cca2."""
    flags = country.get("flags")
    if isinstance(flags, dict) and flags.get("png"):
        return flags.get("png")
    if isinstance(flags, list) and flags:
        return flags[0]
    cca2 = country.get("cca2")
    if cca2:
        return f"https://flagcdn.com/w320/{cca2.lower()}.png"
    return None


def _matches_country(country: Dict[str, Any], query_str: str) -> bool:
    """Check if query matches common name, official name, altSpellings, cca2/cca3, or translations."""
    q = query_str.lower().strip()
    name_obj = country.get("name", {})
    common = str(name_obj.get("common", "")).lower()
    official = str(name_obj.get("official", "")).lower()
    if q in common or q in official:
        return True

    cca2 = str(country.get("cca2", "")).lower()
    cca3 = str(country.get("cca3", "")).lower()
    if q == cca2 or q == cca3:
        return True

    for alt in country.get("altSpellings", []):
        if q in str(alt).lower():
            return True

    for t in country.get("translations", {}).values():
        if isinstance(t, dict):
            if q in str(t.get("common", "")).lower() or q in str(t.get("official", "")).lower():
                return True
    return False


@mcp.tool()
def search_countries(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search countries by name. Returns a list of {name, capital, region, population}.

    Handles empty queries, upstream network errors/timeouts, and no-match scenarios cleanly.
    """
    if not isinstance(query, str) or not query.strip():
        return [{"error": "query must not be empty"}]

    clean_query = query.strip()
    if limit <= 0:
        limit = 5

    raw_countries = []
    # Try upstream REST Countries API first
    try:
        resp = httpx.get(f"{BASE_URL}/name/{clean_query}", follow_redirects=True, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list):
                raw_countries = data
            elif isinstance(data, dict) and isinstance(data.get("data"), list):
                raw_countries = data.get("data")
        elif resp.status_code == 404:
            return []
    except (httpx.HTTPError, httpx.TimeoutException):
        pass

    # If upstream API is deprecated, returns error dict, or empty, fallback to local dataset
    if not raw_countries:
        for c in _load_local_countries():
            if _matches_country(c, clean_query):
                raw_countries.append(c)

    if not raw_countries:
        return []

    results = []
    for c in raw_countries[:limit]:
        cap = c.get("capital")
        capital_val = cap[0] if (isinstance(cap, list) and cap) else (cap if isinstance(cap, str) else None)
        results.append(
            {
                "name": c.get("name", {}).get("common") or c.get("name", {}).get("official"),
                "capital": capital_val,
                "region": c.get("region"),
                "population": c.get("population"),
            }
        )
    return results


@mcp.tool()
def get_country_details(name: str) -> Dict[str, Any]:
    """Get detailed information for a country including currencies, languages, borders, and flag.

    Returns:
      A dictionary containing name, currencies, languages, borders, and flag_url.
      Returns {"error": "..."} on invalid inputs or if the country is not found.
    """
    if not isinstance(name, str) or not name.strip():
        return {"error": "Country name must not be empty"}

    clean_name = name.strip()
    country_data: Optional[Dict[str, Any]] = None

    # Try upstream API
    try:
        resp = httpx.get(f"{BASE_URL}/name/{clean_name}?fullText=true", follow_redirects=True, timeout=3)
        if resp.status_code != 200:
            resp = httpx.get(f"{BASE_URL}/name/{clean_name}", follow_redirects=True, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and data:
                country_data = data[0]
            elif isinstance(data, dict) and isinstance(data.get("data"), list) and data.get("data"):
                country_data = data.get("data")[0]
    except (httpx.HTTPError, httpx.TimeoutException):
        pass

    # Fallback to local dataset
    if not country_data:
        q_lower = clean_name.lower()
        # 1. Exact match pass
        for c in _load_local_countries():
            c_name = c.get("name", {})
            if (
                c_name.get("common", "").lower() == q_lower
                or c_name.get("official", "").lower() == q_lower
                or c.get("cca2", "").lower() == q_lower
                or c.get("cca3", "").lower() == q_lower
                or any(q_lower == str(alt).lower() for alt in c.get("altSpellings", []))
            ):
                country_data = c
                break

        # 2. Substring / translation pass if not found
        if not country_data:
            for c in _load_local_countries():
                if _matches_country(c, clean_name):
                    country_data = c
                    break

    if not country_data:
        return {"error": f"No country found matching '{clean_name}'"}

    # Format currencies: list of {"code": ..., "name": ..., "symbol": ...}
    currencies_dict = country_data.get("currencies") or {}
    currencies_formatted = []
    if isinstance(currencies_dict, dict):
        for code, details in currencies_dict.items():
            if isinstance(details, dict):
                currencies_formatted.append(
                    {
                        "code": code,
                        "name": details.get("name"),
                        "symbol": details.get("symbol"),
                    }
                )
            elif isinstance(details, str):
                currencies_formatted.append({"code": code, "name": details, "symbol": None})

    # Format languages: list of language names
    languages_val = country_data.get("languages") or {}
    if isinstance(languages_val, dict):
        languages_list = list(languages_val.values())
    elif isinstance(languages_val, list):
        languages_list = languages_val
    else:
        languages_list = [str(languages_val)]

    # Format borders: list of bordering country codes
    borders_val = country_data.get("borders") or []
    borders_list = borders_val if isinstance(borders_val, list) else []

    # Flag URL
    flag_url = _get_flag_url(country_data)

    return {
        "name": country_data.get("name", {}).get("common") or country_data.get("name", {}).get("official"),
        "official_name": country_data.get("name", {}).get("official"),
        "currencies": currencies_formatted,
        "languages": languages_list,
        "borders": borders_list,
        "flag_url": flag_url,
    }


if __name__ == "__main__":
    mcp.run()
