"""Data Explorer — MCP server skeleton for Week 4.

Wraps the free, no-key REST Countries API (https://restcountries.com) and exposes it
to an agent as MCP tools over STDIO. One tool is implemented as a worked example;
finish the second (and improve error handling) to complete the assignment.

Setup:
    pip install -r requirements.txt
Run (STDIO) — register this command in your MCP client (e.g. Claude Desktop / an IDE):
    python server.py
"""
import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://restcountries.com/v3.1"
mcp = FastMCP("data-explorer")


@mcp.tool()
def search_countries(query: str, limit: int = 5) -> list[dict]:
    """Search countries by name. Returns a list of {name, capital, region, population}.

    This tool is a WORKED EXAMPLE — study how it validates input, calls the API,
    handles errors, and returns model-friendly data.
    """
    if not query.strip():
        return [{"error": "query must not be empty"}]
    try:
        resp = httpx.get(f"{BASE_URL}/name/{query}", timeout=10)
        if resp.status_code == 404:
            return []  # no matches is not an error
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        return [{"error": f"upstream request failed: {exc}"}]

    results = []
    for c in resp.json()[:limit]:
        results.append(
            {
                "name": c.get("name", {}).get("common"),
                "capital": (c.get("capital") or [None])[0],
                "region": c.get("region"),
                "population": c.get("population"),
            }
        )
    return results


@mcp.tool()
async def get_country_details(name: str) -> dict:
    """Get detailed information for a specific country including currencies, languages, borders, and flag URL.
    
    Args:
        name: Common or official name of a country (e.g., 'Japan', 'France').
    """
    if not name or not name.strip():
        return {"error": "Invalid input: Country name cannot be empty."}

    clean_name = name.strip()
    url = f"{BASE_URL}/name/{clean_name}?fullText=true"

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(url)
            
            # Fallback search if fullText yields no exact match
            if response.status_code == 404:
                fallback_url = f"{BASE_URL}/name/{clean_name}"
                response = await client.get(fallback_url)
                if response.status_code == 404:
                    return {"error": f"Country '{clean_name}' not found."}

            response.raise_for_status()
            data = response.json()
            if not data:
                return {"error": f"No details available for '{clean_name}'."}

            item = data[0]

            currencies_raw = item.get("currencies", {})
            currencies = [
                f"{curr_data.get('name', code)} ({curr_data.get('symbol', '')})".strip()
                for code, curr_data in currencies_raw.items()
            ]

            languages_raw = item.get("languages", {})
            languages = list(languages_raw.values())

            borders = item.get("borders", [])

            flags_raw = item.get("flags", {})
            flag_url = flags_raw.get("png") or flags_raw.get("svg") or "N/A"

            return {
                "name": item.get("name", {}).get("common", clean_name),
                "official_name": item.get("name", {}).get("official", "N/A"),
                "capital": item.get("capital", ["N/A"])[0] if item.get("capital") else "N/A",
                "currencies": currencies if currencies else ["N/A"],
                "languages": languages if languages else ["N/A"],
                "borders": borders if borders else [],
                "flag_url": flag_url
            }

        except httpx.TimeoutException:
            return {"error": "Request timed out while contacting REST Countries API."}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error occurred: {e.response.status_code}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

if __name__ == "__main__":
    mcp.run()
