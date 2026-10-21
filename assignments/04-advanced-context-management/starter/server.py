
"""Week 4 — Data Explorer MCP Server."""

import os
from urllib.parse import quote

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP


load_dotenv()

API_KEY = os.getenv("RESTCOUNTRIES_API_KEY")
BASE_URL = "https://api.restcountries.com/countries/v5"

mcp = FastMCP("data-explorer")


def fetch_countries(name: str, search: bool = False) -> list[dict]:
    """Fetch countries from REST Countries v5.

    search=True uses a name-search query.
    search=False uses the common-name lookup endpoint.
    """

    if not API_KEY:
        raise ValueError("RESTCOUNTRIES_API_KEY is not configured")

    encoded_name = quote(name, safe="")

    if search:
        url = f"{BASE_URL}/names.common?q={encoded_name}"
    else:
        url = f"{BASE_URL}/names.common/{encoded_name}"

    response = httpx.get(
        url,
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=10,
    )

    if response.status_code == 404:
        return []

    response.raise_for_status()

    payload = response.json()

    if not isinstance(payload, dict):
        raise ValueError("Invalid API response")

    data = payload.get("data")

    if not isinstance(data, dict):
        raise ValueError("Invalid API response structure")

    countries = data.get("objects")

    if not isinstance(countries, list):
        raise ValueError("Country list is missing")

    if not all(isinstance(country, dict) for country in countries):
        raise ValueError("Invalid country record")

    return countries


@mcp.tool()
def search_countries(query: str, limit: int = 5) -> list[dict]:
    """Search countries by name.

    Supports partial country-name queries.

    Returns:
        A list containing name, capital, region, and population.
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
        countries = fetch_countries(query.strip(), search=True)
        results = []

        for country in countries[:limit]:
            names = country.get("names") or {}
            capitals = country.get("capitals") or []

            if not isinstance(names, dict) or not isinstance(capitals, list):
                raise ValueError("Invalid country fields")

            capital = None

            if capitals:
                if not isinstance(capitals[0], dict):
                    raise ValueError("Invalid capital record")

                capital = capitals[0].get("name")

            results.append(
                {
                    "name": names.get("common"),
                    "capital": capital,
                    "region": country.get("region"),
                    "population": country.get("population"),
                }
            )

        return results

    except httpx.TimeoutException:
        return [{"error": "API request timed out"}]

    except httpx.HTTPError as exc:
        return [{"error": f"upstream request failed: {exc}"}]

    except (ValueError, TypeError, AttributeError) as exc:
        return [{"error": f"Unable to process country data: {exc}"}]


@mcp.tool()
def get_country_details(name: str) -> dict:
    """Get detailed country information.

    Returns currencies, languages, borders, and flag URL.
    """

    if not isinstance(name, str) or not name.strip():
        return {"error": "name must be a non-empty string"}

    try:
        countries = fetch_countries(name.strip())

        if not countries:
            return {"error": "Country not found"}

        normalized_name = name.strip().casefold()

        # Prefer an exact common-name match.
        country = next(
            (
                item
                for item in countries
                if isinstance(item.get("names"), dict)
                and isinstance(item["names"].get("common"), str)
                and item["names"]["common"].casefold() == normalized_name
            ),
            countries[0],
        )

        names = country.get("names") or {}
        flag = country.get("flag") or {}

        if not isinstance(names, dict) or not isinstance(flag, dict):
            raise ValueError("Invalid country fields")

        currencies = country.get("currencies") or []
        languages = country.get("languages") or []
        borders = country.get("borders") or []

        if not all(
            isinstance(value, list)
            for value in (currencies, languages, borders)
        ):
            raise ValueError("Invalid country details")

        return {
            "name": names.get("common"),
            "currencies": currencies,
            "languages": languages,
            "borders": borders,
            "flag_url": flag.get("url_png"),
        }

    except httpx.TimeoutException:
        return {"error": "API request timed out"}

    except httpx.HTTPError as exc:
        return {"error": f"upstream request failed: {exc}"}

    except (ValueError, TypeError, AttributeError) as exc:
        return {"error": f"Unable to process country data: {exc}"}


if __name__ == "__main__":
    mcp.run()
