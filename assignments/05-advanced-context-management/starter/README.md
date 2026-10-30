# Data Explorer MCP Server

A Model Context Protocol (MCP) server built with `FastMCP` that wraps the open **[mledoze/countries](https://github.com/mledoze/countries)** dataset (the source data REST Countries was built upon) and exposes country search and inspection tools to coding agents over STDIO transport.

---

## Features

- **STDIO Transport**: Connects directly to AI agents and MCP clients (Antigravity, Gemini CLI, Claude Desktop, Cursor).
- **Two Complete Tools**:
  - `search_countries(query, limit=5)`: Case- and accent-insensitive search over common and official country names.
  - `get_country_details(name)`: Rich country profile returning currencies, languages, neighboring borders, and lower-case SVG flag URL.
- **Smart Matching**: Resolves common names, official names, ISO codes (CCA2, CCA3, CIOC), and alternative spellings (e.g. `"Turkey"` or `"Turkiye"` resolves to `"Türkiye"`). Handles ambiguous queries with candidate suggestions.
- **Robust Error Handling**: Never crashes the server process. Returns structured error payloads (`error`, `retryable`) for empty inputs, type mismatches, unknown countries, HTTP errors, and network timeouts.
- **Resilient In-Memory Caching**: Fetches dataset once on demand and caches in memory. Failures are never cached, ensuring subsequent requests seamlessly recover.

---

## Setup & Installation

Ensure you have Python 3.10+ installed:

```bash
cd starter
pip install -r requirements.txt
```

---

## Running the Server

Run directly over STDIO:

```bash
python server.py
```

*Note: The server communicates via JSON-RPC over STDIO. It will wait silently for incoming client messages on standard input.*

---

## Client Registration

### 1. Antigravity / Gemini CLI (`.gemini/settings.json`)

```json
{
  "mcpServers": {
    "data-explorer": {
      "command": "python",
      "args": ["/absolute/path/to/starter/server.py"]
    }
  }
}
```

### 2. Claude Desktop (`claude_desktop_config.json`)

On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`  
On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "data-explorer": {
      "command": "python",
      "args": ["/absolute/path/to/starter/server.py"]
    }
  }
}
```

---

## Tool Reference

### 1. `search_countries`

Search the dataset for countries matching a given query string.

- **Parameters**:
  - `query` (`string`, required): Name or partial name of the country (case-insensitive, accent-insensitive).
  - `limit` (`integer`, optional, default `5`, max `50`): Maximum number of results to return.
- **Return Type**: `list[dict]`
- **Success Example**:
  - **Input**:
    ```json
    {
      "query": "germany",
      "limit": 1
    }
    ```
  - **Output**:
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
- **No Matches**: Returns an empty list `[]`.
- **Error Examples**:
  - Empty query: `[{"error": "query must be a non-empty string"}]`
  - Invalid limit: `[{"error": "limit must be a positive integer"}]`
  - Upstream timeout: `[{"error": "upstream request timed out", "retryable": true}]`

---

### 2. `get_country_details`

Retrieve full details for a specified country, including currencies, languages, bordering nations, and flag asset URL.

- **Parameters**:
  - `name` (`string`, required): Country name, official name, 2/3-letter ISO code, or alternative spelling.
- **Return Type**: `dict`
- **Success Example**:
  - **Input**:
    ```json
    {
      "name": "Turkey"
    }
    ```
  - **Output**:
    ```json
    {
      "name": "Türkiye",
      "official_name": "Republic of Turkey",
      "cca2": "TR",
      "cca3": "TUR",
      "currencies": {
        "TRY": {
          "name": "Turkish lira",
          "symbol": "₺"
        }
      },
      "languages": {
        "tur": "Turkish"
      },
      "borders": [
        "ARM",
        "AZE",
        "BGR",
        "GEO",
        "GRC",
        "IRN",
        "IRQ",
        "SYR"
      ],
      "flag_url": "https://raw.githubusercontent.com/mledoze/countries/master/data/tur.svg"
    }
    ```
- **Error Examples**:
  - Country not found: `{"error": "country 'Atlantis' not found"}`
  - Ambiguous query: `{"error": "ambiguous country name 'Dominic', multiple matches found", "candidates": ["Dominica", "Dominican Republic"]}`
  - Empty input: `{"error": "name must be a non-empty string"}`
  - Upstream network failure: `{"error": "upstream request failed: ...", "retryable": true}`

---

## Running the Test Suite

Run unit and integration tests using pytest:

```bash
pytest
```

All 22 unit and regression tests run completely offline and verify input validation, smart matching, error formats, and recovery behaviors.
