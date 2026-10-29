"""Data Explorer — MCP server skeleton for Week 5.

Wraps an open country dataset and exposes it to an agent as MCP tools over STDIO.
One tool is implemented as a worked example; finish the second (and improve error
handling) to complete the assignment.

Data source: the open `mledoze/countries` dataset (the data REST Countries was built
on), served as one JSON file from GitHub. No API key. It is fetched over HTTPS on the
first call and cached in memory, so HTTP errors and timeouts are still real failure
modes your tools must handle.

Setup:
    pip install -r requirements.txt
Run (STDIO) — register this command in your MCP client (e.g. Claude Desktop / an IDE):
    python server.py
"""
import httpx
from mcp.server.fastmcp import FastMCP

DATA_URL = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"
# Each country has a 3-letter `cca3` code; its flag lives at this URL.
FLAG_URL = "https://raw.githubusercontent.com/mledoze/countries/master/data/{cca3}.svg"

mcp = FastMCP("data-explorer")

_countries: list[dict] | None = None  # in-memory cache of the dataset


def load_countries() -> list[dict]:
    """Download the dataset once and cache it. Raises httpx.HTTPError on failure."""
    global _countries
    if _countries is None:
        resp = httpx.get(DATA_URL, timeout=30, follow_redirects=True)
        resp.raise_for_status()
        _countries = resp.json()
    return _countries


@mcp.tool()
def search_countries(query: str, limit: int = 5) -> list[dict]:
    """Search countries by name. Returns a list of {name, capital, region, subregion}.

    This tool is a WORKED EXAMPLE — study how it validates input, fetches the data,
    handles errors, and returns model-friendly data.
    """
    if not query.strip():
        return [{"error": "query must not be empty"}]
    try:
        countries = load_countries()
    except httpx.HTTPError as exc:
        return [{"error": f"upstream request failed: {exc}"}]

    q = query.strip().lower()
    matches = [
        c for c in countries
        if q in c["name"]["common"].lower() or q in c["name"]["official"].lower()
    ]
    # No matches is not an error: return an empty list.
    results = []
    for c in matches[:limit]:
        results.append(
            {
                "name": c["name"]["common"],
                "capital": (c.get("capital") or [None])[0],
                "region": c.get("region"),
                "subregion": c.get("subregion"),
            }
        )
    return results


@mcp.tool()
def get_country_details(name: str) -> dict:
    """Get detailed information about a country including currencies, languages, borders, and flag URL."""
    if not name or not name.strip():
        return {"error": "name must not be empty"}
        
    try:
        countries = load_countries()
    except httpx.HTTPError as exc:
        return {"error": f"upstream request failed: {exc}"}
        
    q = name.strip().lower()
    for c in countries:
        common = c.get("name", {}).get("common", "").lower()
        official = c.get("name", {}).get("official", "").lower()
        
        if q == common or q == official:
            # Currencies: map object to list of formatted strings or dictionary
            currencies = c.get("currencies", {})
            languages = list(c.get("languages", {}).values()) if c.get("languages") else []
            borders = c.get("borders", [])
            cca3 = c.get("cca3", "").lower()
            flag_url = FLAG_URL.format(cca3=cca3) if cca3 else ""
            
            return {
                "name": c.get("name", {}).get("common"),
                "currencies": currencies,
                "languages": languages,
                "borders": borders,
                "flag_url": flag_url
            }
            
    return {"error": f"country '{name}' not found"}


if __name__ == "__main__":
    mcp.run()
