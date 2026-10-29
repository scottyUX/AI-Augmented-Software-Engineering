
"""Week 5 — Data Explorer MCP Server.

Exposes country search and country details as MCP tools.
Uses the open mledoze/countries dataset from GitHub.
"""

import httpx
from mcp.server.fastmcp import FastMCP


DATA_URL = (
    "https://raw.githubusercontent.com/"
    "mledoze/countries/master/countries.json"
)

FLAG_URL = (
    "https://raw.githubusercontent.com/"
    "mledoze/countries/master/data/{cca3}.svg"
)

mcp = FastMCP("data-explorer")

_countries: list[dict] | None = None


def load_countries() -> list[dict]:
    """Download and cache the country dataset."""
    global _countries

    if _countries is None:
        response = httpx.get(
            DATA_URL,
            timeout=30,
            follow_redirects=True,
        )
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            raise ValueError("Invalid country dataset")

        if not all(isinstance(country, dict) for country in data):
            raise ValueError("Invalid country record")

        _countries = data

    return _countries


@mcp.tool()
def search_countries(query: str, limit: int = 5) -> list[dict]:
    """Search countries by name.

    Returns name, capital, region, and subregion.
    """

    if not isinstance(query, str) or not query.strip():
        return [{"error": "query must be a non-empty string"}]

    if (
        not isinstance(limit, int)
        or isinstance(limit, bool)
        or not 1 <= limit <= 20
    ):
        return [{"error": "limit must be an integer between 1 and 20"}]

    try:
        countries = load_countries()

        normalized_query = query.strip().casefold()

        matches = [
            country
            for country in countries
            if normalized_query
            in country["name"]["common"].casefold()
            or normalized_query
            in country["name"]["official"].casefold()
        ]

        results = []

        for country in matches[:limit]:
            results.append(
                {
                    "name": country["name"]["common"],
                    "capital": (
                        country.get("capital") or [None]
                    )[0],
                    "region": country.get("region"),
                    "subregion": country.get("subregion"),
                }
            )

        return results

    except httpx.TimeoutException:
        return [{"error": "upstream request timed out"}]

    except httpx.HTTPError as exc:
        return [{"error": f"upstream request failed: {exc}"}]

    except (ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
        return [{"error": f"Unable to process country data: {exc}"}]


@mcp.tool()
def get_country_details(name: str) -> dict:
    """Get country details.

    Returns currencies, languages, borders, and flag URL.
    """

    if not isinstance(name, str) or not name.strip():
        return {"error": "name must be a non-empty string"}

    try:
        countries = load_countries()

        normalized_name = name.strip().casefold()

        country = next(
            (
                item
                for item in countries
                if item["name"]["common"].casefold()
                == normalized_name
                or item["name"]["official"].casefold()
                == normalized_name
            ),
            None,
        )

        if country is None:
            return {"error": "Country not found"}

        cca3 = country.get("cca3")

        return {
            "name": country["name"]["common"],
            "currencies": country.get("currencies") or {},
            "languages": country.get("languages") or {},
            "borders": country.get("borders") or [],
            "flag_url": (
                FLAG_URL.format(cca3=cca3.lower())
                if cca3
                else None
            ),
        }

    except httpx.TimeoutException:
        return {"error": "upstream request timed out"}

    except httpx.HTTPError as exc:
        return {"error": f"upstream request failed: {exc}"}

    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        return {"error": f"Unable to process country data: {exc}"}


if __name__ == "__main__":
    mcp.run()
