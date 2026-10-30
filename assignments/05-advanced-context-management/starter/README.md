# Data Explorer MCP Server

## Overview

Data Explorer is a Python-based Model Context Protocol (MCP) server built using FastMCP. It provides country information from the open-source mledoze/countries dataset hosted on GitHub.

The server uses STDIO transport and exposes two tools to AI agents: `search_countries` and `get_country_details`.

## Requirements

- Python 3.10 or later
- pip
- An MCP-compatible client, such as VS Code with GitHub Copilot
- Internet connection for the initial dataset download

## Installation

Clone the repository and navigate to the starter directory.

```bash
cd assignments/05-advanced-context-management/starter
python -m pip install -r requirements.txt
```

## Running the Server

```bash
python server.py
```

The server communicates through STDIO. It is normal for the terminal to remain idle without displaying output.

## MCP Client Configuration

In VS Code, create `.vscode/mcp.json` inside the starter directory:

```json
{
  "servers": {
    "data-explorer": {
      "type": "stdio",
      "command": "python",
      "args": ["${workspaceFolder}/server.py"]
    }
  }
}
```

Open the starter directory as the VS Code workspace. Use the MCP server controls to start `data-explorer`.

In GitHub Copilot Chat, select Agent mode and invoke the tools.

## Tool Reference

### 1. search_countries

Searches for countries by their common or official names.

**Parameters:**

- `query` (string, required): Country name or partial name.
- `limit` (integer, optional): Maximum number of results, from 1 to 50. Default is 5.

**Example input:**

```json
{
  "query": "Türkiye",
  "limit": 5
}
```

**Example output:**

```json
{
  "success": true,
  "count": 1,
  "results": [
    {
      "name": "Türkiye",
      "capital": "Ankara",
      "region": "Asia",
      "subregion": "Western Asia"
    }
  ],
  "message": "Countries found."
}
```

A valid query with no matches returns `success: true`, `count: 0`, and an empty results list.

### 2. get_country_details

Retrieves detailed information about a country using its common name, official name, or three-letter country code.

**Parameters:**

- `name` (string, required): Exact country name or CCA3 country code.

**Example input:**

```json
{
  "name": "Germany"
}
```

**Example output:**

```json
{
  "success": true,
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

Border values are three-letter country codes. The flag URL points to an SVG file.

## Error Handling

Both tools return structured JSON responses instead of allowing expected errors to crash the server.

Handled cases include:

- Empty or invalid input (`INVALID_INPUT`)
- Invalid search limits (`INVALID_LIMIT`)
- Unknown country names (`NOT_FOUND`)
- Request timeouts (`TIMEOUT`)
- Upstream HTTP errors (`HTTP_ERROR`)
- Network failures (`NETWORK_ERROR`)
- Invalid dataset content (`DATA_ERROR`)

Example:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Query must be a non-empty string."
  }
}
```

The country dataset is downloaded over HTTPS and cached in memory after the first successful request.

## Data Source

https://github.com/mledoze/countries

## Transport

STDIO only. No remote hosting or API authentication is required.