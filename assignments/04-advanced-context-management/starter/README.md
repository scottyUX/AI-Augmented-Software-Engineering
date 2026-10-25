# Starter — Data Explorer MCP Server

A Model Context Protocol (MCP) server implementing **FastMCP** over standard country data (REST Countries schema with resilient offline fallback). Exposes two typed tools to LLM agents over STDIO with robust error handling and model-friendly output structures.

---

## Setup

1. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Requires `mcp<2`, `httpx`, and optionally `pytest` for tests).*

---

## Run (STDIO)

```bash
python server.py
```
This starts the FastMCP server over standard I/O (STDIO).

---

## Register in MCP Clients

### Claude Desktop
Add to your Claude Desktop configuration (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "data-explorer": {
      "command": "/absolute/path/to/starter/.venv/bin/python",
      "args": ["/absolute/path/to/starter/server.py"]
    }
  }
}
```

### Cursor / VS Code / Antigravity / Any MCP-compatible IDE
Configure standard STDIO transport with:
- **Command:** `<path_to_starter>/.venv/bin/python`
- **Args:** `["<path_to_starter>/server.py"]`

---

## Tool Reference

### 1. `search_countries`
Search countries by common name, official name, or translation.

- **Parameters:**
  - `query` (`str`, required): Name or keyword to search for. Must not be empty.
  - `limit` (`int`, optional, default: 5): Maximum number of results to return.
- **Return Shape:**
  ```json
  [
    {
      "name": "Türkiye",
      "capital": "Ankara",
      "region": "Asia",
      "population": 84339067
    }
  ]
  ```
- **Error Behavior:**
  - Empty string: returns `[{"error": "query must not be empty"}]`.
  - No match found: returns `[]`.

---

### 2. `get_country_details`
Retrieve comprehensive details for a specific country including currencies, official languages, border countries, and flag URLs.

- **Parameters:**
  - `name` (`str`, required): Country name, code (CCA2/CCA3), or spelling variant.
- **Return Shape:**
  ```json
  {
    "name": "Germany",
    "official_name": "Federal Republic of Germany",
    "currencies": [
      {
        "code": "EUR",
        "name": "Euro",
        "symbol": "€"
      }
    ],
    "languages": [
      "German"
    ],
    "borders": [
      "AUT", "BEL", "CZE", "DNK", "FRA", "LUX", "NLD", "POL", "CHE"
    ],
    "flag_url": "https://flagcdn.com/w320/de.png"
  }
  ```
- **Error Behavior:**
  - Empty string: returns `{"error": "Country name must not be empty"}`.
  - Country not found: returns `{"error": "No country found matching '<name>'"}`.

---

## Running Automated Tests

Run the test suite covering tool outputs and edge-case error scenarios:
```bash
pytest test_server.py
```
