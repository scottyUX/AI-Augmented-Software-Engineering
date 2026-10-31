# Data Explorer MCP Server

A `FastMCP` server over the open **[mledoze/countries](https://github.com/mledoze/countries)** dataset that exposes country search and details tools over STDIO.

## Setup
```bash
pip install -r requirements.txt
```

## Run (STDIO)
```bash
python server.py
```

## Register in MCP Client (Claude Desktop / Antigravity)
Add to your client config:
```json
{
  "mcpServers": {
    "data-explorer": {
      "command": "python",
      "args": ["/absolute/path/to/server.py"]
    }
  }
}
```

## Tool Reference

### `search_countries(query: str, limit: int = 5)`
Search countries by name. Returns `{name, capital, region, subregion}`.

- **Example Input:** `{"query": "germany", "limit": 1}`
- **Example Output:**
  ```json
  [
    {
      "name": "Germany",
      "capital": "Berlin",
      "region": "Europe",
      "subregion": "Western Europe"
    }
  ]
  ```
- **Error (Empty Input):** `[{"error": "query must not be empty"}]`

### `get_country_details(name: str)`
Get details for a country: currencies, languages, borders, and flag SVG URL.

- **Example Input:** `{"name": "germany"}`
- **Example Output:**
  ```json
  {
    "name": "Germany",
    "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
    "languages": {"deu": "German"},
    "borders": ["AUT", "BEL", "CZE", "DNK", "FRA", "LUX", "NLD", "POL", "CHE"],
    "flag": "https://raw.githubusercontent.com/mledoze/countries/master/data/deu.svg"
  }
  ```
- **Error (Not Found):** `{"error": "no country found for 'Atlantis'"}`
