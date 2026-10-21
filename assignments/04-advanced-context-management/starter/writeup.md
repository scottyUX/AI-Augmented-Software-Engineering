# Week 4 — Data Explorer MCP Server Writeup

## 1. Implementation Overview

For this assignment, I extended the provided FastMCP server by improving the existing `search_countries(query, limit=5)` tool and implementing `get_country_details(name)`.

During development, I discovered that the REST Countries API v3.1 endpoint used in the starter code had been deprecated. Therefore, I migrated the implementation to REST Countries API v5 and configured API key authentication using a local `.env` file and `python-dotenv`.

The server communicates over STDIO transport and exposes the two tools required by the assignment.

## 2. AI Agent MCP Tool Invocation Transcript

I registered the `data-explorer` MCP server in Antigravity IDE using STDIO transport. I instructed the AI agent to invoke both tools directly rather than answering from its own knowledge or making separate HTTP requests.

The following transcript contains the tool names, input arguments, and results reported by the Antigravity agent.

### Tool Call 1 — `search_countries`

**MCP Server:** `data-explorer`

**Tool Name:** `search_countries`

**Input Arguments:**

```json
{
  "query": "Germany",
  "limit": 5
}
```

**Returned Result:**

```json
{
  "name": "Germany",
  "capital": "Berlin",
  "region": "Europe",
  "population": 83298787
}
```

### Tool Call 2 — `get_country_details`

**MCP Server:** `data-explorer`

**Tool Name:** `get_country_details`

**Input Arguments:**

```json
{
  "name": "Germany"
}
```

**Returned Result:**

```json
{
  "name": "Germany",
  "currencies": [
    {
      "code": "EUR",
      "name": "Euro",
      "symbol": "€"
    }
  ],
  "languages": [
    {
      "bcp47": "de",
      "iso639_1": "de",
      "iso639_2b": "ger",
      "iso639_2t": "deu",
      "iso639_3": "deu",
      "name": "German",
      "native_name": "Deutsch"
    }
  ],
  "borders": [
    "AUT",
    "BEL",
    "CZE",
    "DNK",
    "FRA",
    "LUX",
    "NLD",
    "POL",
    "CHE"
  ],
  "flag_url": "https://flags.restcountries.com/v5/w640/de.png"
}
```

Both tools were successfully invoked through the connected MCP server, allowing the agent to retrieve country information from the external API.

## 3. Error Handling

I implemented input validation and exception handling in both tools to ensure that invalid inputs and API failures return structured error messages instead of crashing the server.

The following scenarios were tested:

| Test Case | Returned Result |
|---|---|
| Empty search query | `query must be a non-empty string` |
| Invalid result limit | `limit must be an integer between 1 and 20` |
| Empty country name | `name must be a non-empty string` |
| Invalid query type (`None`) | `query must be a non-empty string` |
| Unknown country search | Empty list `[]` |
| Unknown country details | `Country not found` |
| Simulated request timeout | `API request timed out` |
| Simulated connection failure | `upstream request failed: Simulated connection failure` |

Timeout and connection failure scenarios were simulated using Python's built-in `unittest.mock` module.

The implementation also checks HTTP response status codes and validates the structure of the returned JSON data before processing it.

## 4. Reflection

This assignment helped me understand how MCP servers allow AI agents to access external information through clearly defined tools. I learned that defining tool names, parameters, and return structures helps control what context an agent can request and receive. Implementing input validation and error handling showed me how to make external data access more reliable and predictable. Connecting the server to Antigravity and observing the agent invoke both tools helped me understand how STDIO transport enables communication between an AI agent and an MCP server.