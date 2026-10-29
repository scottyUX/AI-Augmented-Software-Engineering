# Week 5 — Data Explorer MCP Server

A custom Model Context Protocol (MCP) server built with FastMCP. The server provides two tools for searching countries and retrieving country details.

The server uses the open [mledoze/countries](https://github.com/mledoze/countries) dataset hosted on GitHub. No API key is required.

## Setup

Requirements:
- Python 3.10 or later
- Dependencies listed in `requirements.txt`

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run (STDIO)

```powershell
python server.py
```

The server uses STDIO transport. It waits for an MCP client to connect and does not provide an interactive command-line interface.

## Register in VS Code

The server was registered in Visual Studio Code using the MCP Servers configuration.

Example user-level `mcp.json` configuration:

```json
{
  "servers": {
    "data-explorer": {
      "type": "stdio",
      "command": "C:\\path\\to\\starter\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\path\\to\\starter\\server.py"
      ]
    }
  }
}
```

Replace the example paths with the absolute paths on your machine.

Start the `data-explorer` server in VS Code, open Copilot Chat in Agent mode, and enable both MCP tools.

## Tool Reference

### 1. search_countries

Searches countries by their common or official names.

**Parameters:**

- `query` (string, required): Country name or partial name.
- `limit` (integer, optional): Maximum number of results. Defaults to 5; valid range is 1–20.

**Example input:**

```json
{
  "query": "Germany",
  "limit": 5
}
```

**Example output:**

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

Returns an empty list when no countries match the query.

### 2. get_country_details

Retrieves detailed information about a country by its common or official name.

**Parameters:**

- `name` (string, required): Country name.

**Example input:**

```json
{
  "name": "Germany"
}
```

**Example output:**

```json
{
  "name": "Germany",
  "currencies": {
    "EUR": {
      "name": "Euro",
      "symbol": "€"
    }
  },
  "languages": {
    "deu": "German"
  },
  "borders": [
    "AUT", "BEL", "CZE", "DNK", "FRA",
    "LUX", "NLD", "POL", "CHE"
  ],
  "flag_url": "https://raw.githubusercontent.com/mledoze/countries/master/data/deu.svg"
}
```

Returns a structured error message when the country is not found.

## Error Handling

Both tools handle invalid or empty input, upstream HTTP errors, request timeouts, and invalid data structures without crashing the server.

Examples:

```json
{"error": "name must be a non-empty string"}
```

```json
{"error": "Country not found"}
```

```json
{"error": "upstream request timed out"}
```

For `search_countries`, error messages are returned inside a list.

## MCP Client Testing

Both tools were successfully invoked from GitHub Copilot Chat in VS Code Agent mode.

The actual tool-call transcript, error-handling tests, and reflection are documented in `writeup.md`.
