# Week 5 — Data Explorer MCP Server Writeup

## 1. Overview

In this assignment, I completed a custom MCP server using Python and FastMCP. The server connects to the open-source mledoze/countries dataset on GitHub and provides two tools for an AI agent.

I implemented `get_country_details`, improved error handling for both tools, and connected the server to GitHub Copilot in Visual Studio Code using STDIO transport.

## 2. MCP Agent Tool Call Transcript

The following tool calls were executed through GitHub Copilot Chat in Agent mode.

### Test 1 — search_countries

**Agent request:**

Use the data-explorer MCP server's search_countries tool with query "Türkiye" and limit 5.

**Tool called:** `search_countries`

**Input:**

```json
{
  "query": "Türkiye",
  "limit": 5
}
```

**Actual tool response:**

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

**Result:** Successful. The MCP tool returned the matching country information.

### Test 2 — get_country_details

**Agent request:**

Use the get_country_details MCP tool to get information about Germany. Show the complete JSON response.

**Tool called:** `get_country_details`

**Input:**

```json
{
  "name": "Germany"
}
```

**Actual tool response:**

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
  "flag_url": "https://raw.githubusercontent.com/mledoze/countries/master/data/deu.svg"
}
```

**Result:** Successful. The MCP tool returned currencies, languages, neighboring country codes, and a flag URL.

## 3. Error Handling and Validation

I added input validation and structured error responses to prevent expected failures from crashing the MCP server.

The following error cases were tested through GitHub Copilot.

### Test 3 — Empty Search Query

**Input:**

```json
{
  "query": "",
  "limit": 5
}
```

**Response:**

```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Query must be a non-empty string."
  }
}
```

**Result:** Successful. The tool rejected an empty search query.

### Test 4 — Invalid Search Limit

**Input:**

```json
{
  "query": "Germany",
  "limit": -1
}
```

**Response:**

```json
{
  "success": false,
  "error": {
    "code": "INVALID_LIMIT",
    "message": "Limit must be an integer between 1 and 50."
  }
}
```

**Result:** Successful. The tool rejected an invalid search limit.

### Test 5 — Country Not Found

**Input:**

```json
{
  "name": "NonexistentCountry123"
}
```

**Response:**

```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "No country found with the name 'NonexistentCountry123'."
  }
}
```

**Result:** Successful. The tool returned a structured error when the requested country was not found.

### Test 6 — No Matching Countries

**Tool called:** `search_countries`

**Input:**

```json
{
  "query": "xyznonexistent123",
  "limit": 5
}
```

**Actual tool response:**

```json
{
  "success": true,
  "count": 0,
  "results": [],
  "message": "No matching countries found."
}
```

**Result:** Successful. The tool handled a search with no matches by returning an empty results list without crashing.

### Additional Upstream Error Tests

I created `test_server.py` using Python's `unittest.mock` to simulate external API failures.

The following tests were executed successfully:

- Search timeout: PASS (`TIMEOUT`)
- HTTP 503 error: PASS (`HTTP_ERROR`)
- Network connection failure: PASS (`NETWORK_ERROR`)

**Terminal output:**

```text
PASS: Search timeout (TIMEOUT)
PASS: Country details HTTP error (HTTP_ERROR)
PASS: Network error (NETWORK_ERROR)
All upstream error tests passed!
```

All three tests passed successfully.

The server returned structured error responses without crashing. These tests used mocked HTTP requests rather than real network failures.

The implementation also includes validation of the downloaded dataset and in-memory caching to avoid unnecessary repeated HTTP requests.

## 4. Context Management Reflection

I learned that MCP servers allow AI agents to access external information through clearly defined tools. By exposing only specific functions, such as searching for countries and retrieving country details, developers can control what information an agent is allowed to access. Structured tool responses help the agent understand the retrieved data while reducing unnecessary context. I also learned that input validation and error handling are important for making external data access reliable. Overall, MCP provides a practical way to extend an AI agent's capabilities without giving it unrestricted access to external systems.

## 5. Conclusion

The Data Explorer MCP server was successfully registered in Visual Studio Code and accessed through GitHub Copilot Chat using STDIO transport.

Both MCP tools were executed successfully, and the tested invalid inputs returned structured error responses. Additional timeout, HTTP, and network failure scenarios were verified using mocked requests.

The server retrieves country information from the open-source mledoze/countries dataset and requires no API key.

This assignment helped me understand how MCP tools can extend an AI agent's access to external data while maintaining controlled, structured, and reliable interactions.