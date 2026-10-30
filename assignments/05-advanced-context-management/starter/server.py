"""Data Explorer — MCP server for Week 5.

Wraps the open mledoze/countries dataset and exposes it to an agent as MCP tools over STDIO.
Provides two tools:
- `search_countries(query, limit=5)`: Search countries by name.
- `get_country_details(name)`: Get detailed info (currencies, languages, borders, flag URL).

Run (STDIO):
    python server.py
"""
import unicodedata
import httpx
from mcp.server.fastmcp import FastMCP

DATA_URL = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"
# Each country has a 3-letter `cca3` code; its flag lives at this URL (in lowercase).
FLAG_URL = "https://raw.githubusercontent.com/mledoze/countries/master/data/{cca3}.svg"

mcp = FastMCP("data-explorer")

_countries: list[dict] | None = None  # in-memory cache of the dataset


def normalize_text(text: str) -> str:
    """Normalize text by lowercasing and stripping diacritics/accents."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower().strip()


def load_countries() -> list[dict]:
    """Download the dataset once and cache it in memory.

    Raises httpx.HTTPError on network or upstream failures.
    Does not cache failures so future calls can retry.
    """
    global _countries
    if _countries is None:
        resp = httpx.get(DATA_URL, timeout=30, follow_redirects=True)
        resp.raise_for_status()
        data = resp.json()
        if not isinstance(data, list):
            raise ValueError("Unexpected dataset format: expected a JSON list")
        _countries = data
    return _countries


def find_country(name: str, countries: list[dict]) -> tuple[dict | None, list[str]]:
    """Find a country by exact or partial match.

    Returns:
        (country_dict, []) if exactly one matched.
        (None, candidates) if multiple partial matches found (ambiguous).
        (None, []) if no match found.
    """
    target = normalize_text(name)
    if not target:
        return None, []

    # 1. Exact match check (common name, official name, codes, alt spellings)
    for c in countries:
        common = normalize_text(c.get("name", {}).get("common", ""))
        official = normalize_text(c.get("name", {}).get("official", ""))
        cca2 = normalize_text(c.get("cca2", ""))
        cca3 = normalize_text(c.get("cca3", ""))
        cioc = normalize_text(c.get("cioc", ""))

        if target in (common, official, cca2, cca3, cioc):
            return c, []

        alt_spellings = [normalize_text(alt) for alt in c.get("altSpellings", [])]
        if target in alt_spellings:
            return c, []

    # 2. Substring / partial match fallback
    partial_matches = []
    for c in countries:
        common = normalize_text(c.get("name", {}).get("common", ""))
        official = normalize_text(c.get("name", {}).get("official", ""))
        alt_spellings = [normalize_text(alt) for alt in c.get("altSpellings", [])]

        if target in common or target in official or any(target in alt for alt in alt_spellings):
            partial_matches.append(c)

    if len(partial_matches) == 1:
        return partial_matches[0], []
    elif len(partial_matches) > 1:
        candidates = [c.get("name", {}).get("common", "Unknown") for c in partial_matches]
        return None, candidates

    return None, []


@mcp.tool()
def search_countries(query: str, limit: int = 5) -> list[dict]:
    """Search countries by name. Returns a list of {name, capital, region, subregion}.

    Args:
        query: Country name or partial name to search for (case-insensitive).
        limit: Maximum number of results to return (default 5, maximum 50).
    """
    if not isinstance(query, str) or not query.strip():
        return [{"error": "query must be a non-empty string"}]

    if not isinstance(limit, int) or limit < 1:
        return [{"error": "limit must be a positive integer"}]

    limit = min(limit, 50)

    try:
        countries = load_countries()
    except httpx.TimeoutException:
        return [{"error": "upstream request timed out", "retryable": True}]
    except httpx.HTTPError as exc:
        return [{"error": f"upstream request failed: {exc}", "retryable": True}]
    except Exception as exc:
        return [{"error": f"failed to load country dataset: {exc}", "retryable": False}]

    target = normalize_text(query)
    matches = []
    for c in countries:
        common = normalize_text(c.get("name", {}).get("common", ""))
        official = normalize_text(c.get("name", {}).get("official", ""))
        alt_spellings = [normalize_text(alt) for alt in c.get("altSpellings", [])]

        if target in common or target in official or any(target in alt for alt in alt_spellings):
            matches.append(c)

    results = []
    for c in matches[:limit]:
        results.append(
            {
                "name": c.get("name", {}).get("common"),
                "capital": (c.get("capital") or [None])[0],
                "region": c.get("region"),
                "subregion": c.get("subregion"),
            }
        )
    return results


@mcp.tool()
def get_country_details(name: str) -> dict:
    """Get detailed information about a country including currencies, languages, borders, and flag URL.

    Args:
        name: Common name, official name, ISO code (CCA2/CCA3), or alternative spelling of the country.
    """
    if not isinstance(name, str) or not name.strip():
        return {"error": "name must be a non-empty string"}

    try:
        countries = load_countries()
    except httpx.TimeoutException:
        return {"error": "upstream request timed out", "retryable": True}
    except httpx.HTTPError as exc:
        return {"error": f"upstream request failed: {exc}", "retryable": True}
    except Exception as exc:
        return {"error": f"failed to load country dataset: {exc}", "retryable": False}

    country, candidates = find_country(name, countries)

    if country is None:
        if candidates:
            return {
                "error": f"ambiguous country name '{name}', multiple matches found",
                "candidates": candidates[:10],
            }
        return {"error": f"country '{name}' not found"}

    cca3 = (country.get("cca3") or "").lower()
    flag_url = FLAG_URL.format(cca3=cca3) if cca3 else None

    return {
        "name": country.get("name", {}).get("common"),
        "official_name": country.get("name", {}).get("official"),
        "cca2": country.get("cca2"),
        "cca3": country.get("cca3"),
        "currencies": country.get("currencies") or {},
        "languages": country.get("languages") or {},
        "borders": country.get("borders") or [],
        "flag_url": flag_url,
    }


if __name__ == "__main__":
    mcp.run()
