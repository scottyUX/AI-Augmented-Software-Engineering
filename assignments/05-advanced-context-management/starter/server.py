
"""Week 5 - Data Explorer MCP Server."""

import httpx
from mcp.server.fastmcp import FastMCP

DATA_URL = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"
FLAG_URL = "https://raw.githubusercontent.com/mledoze/countries/master/data/{cca3}.svg"

mcp = FastMCP("data-explorer")

_countries: list[dict] | None = None


def load_countries() -> list[dict]:
    """Fetch and cache country data."""
    global _countries

    if _countries is None:
        response = httpx.get(
            DATA_URL,
            timeout=30,
            follow_redirects=True
        )
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, list):
            raise ValueError("Invalid country dataset format")

        _countries = data

    return _countries


def error_response(code: str, message: str) -> dict:
    """Return a structured error response."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }


def fetch_data() -> tuple[list[dict] | None, dict | None]:
    """Load countries and handle upstream errors."""
    try:
        return load_countries(), None
    except httpx.TimeoutException:
        return None, error_response(
            "TIMEOUT",
            "The country data request timed out."
        )
    except httpx.HTTPStatusError as exc:
        return None, error_response(
            "HTTP_ERROR",
            f"Upstream API returned HTTP {exc.response.status_code}."
        )
    except httpx.RequestError:
        return None, error_response(
            "NETWORK_ERROR",
            "Unable to connect to the country data source."
        )
    except (ValueError, TypeError):
        return None, error_response(
            "DATA_ERROR",
            "The country dataset could not be processed."
        )


@mcp.tool()
def search_countries(query: str, limit: int = 5) -> dict:
    """Search countries by name and return basic information."""

    if not isinstance(query, str) or not query.strip():
        return error_response(
            "INVALID_INPUT",
            "Query must be a non-empty string."
        )

    if type(limit) is not int or limit < 1 or limit > 50:
        return error_response(
            "INVALID_LIMIT",
            "Limit must be an integer between 1 and 50."
        )

    countries, error = fetch_data()

    if error is not None:
        return error

    q = query.strip().casefold()
    results = []

    for country in countries:
        names = country.get("name") or {}
        common = names.get("common") or ""
        official = names.get("official") or ""

        if q in common.casefold() or q in official.casefold():
            results.append({
                "name": common,
                "capital": (country.get("capital") or [None])[0],
                "region": country.get("region"),
                "subregion": country.get("subregion")
            })

        if len(results) >= limit:
            break

    return {
        "success": True,
        "count": len(results),
        "results": results,
        "message": (
            "Countries found."
            if results else "No matching countries found."
        )
    }


@mcp.tool()
def get_country_details(name: str) -> dict:
    """Get currencies, languages, borders and flag URL."""

    if not isinstance(name, str) or not name.strip():
        return error_response(
            "INVALID_INPUT",
            "Country name must be a non-empty string."
        )

    countries, error = fetch_data()

    if error is not None:
        return error

    q = name.strip().casefold()

    country = next(
        (
            c for c in countries
            if q == (c.get("name") or {}).get("common", "").casefold()
            or q == (c.get("name") or {}).get("official", "").casefold()
            or q == (c.get("cca3") or "").casefold()
        ),
        None
    )

    if country is None:
        return error_response(
            "NOT_FOUND",
            f"No country found with the name '{name}'."
        )

    code = country.get("cca3")

    return {
        "success": True,
        "name": country["name"]["common"],
        "currencies": country.get("currencies") or {},
        "languages": country.get("languages") or {},
        "borders": country.get("borders") or [],
        "flag_url": (
            FLAG_URL.format(cca3=code.lower())
            if code else None
        )
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
