# Week 4 — Writeup: Custom MCP Server (The Data Explorer)

## 1. Overview
This writeup documents the implementation, error-handling strategy, client verification transcripts, and architectural reflection for the **Data Explorer MCP Server** built using `FastMCP` over STDIO transport.

---

## 2. Agent / MCP Client Session Transcript
The server was driven over standard STDIO using an automated MCP client session (`mcp_client_runner.py`), simulating real agent interactions with initialization, tool discovery, and tool invocations.

### A. Server Initialization & Tool Discovery
```json
{
  "step": "initialize",
  "server": "data-explorer",
  "version": "1.30.0"
}
```
Available tools discovered by the client:
```json
{
  "step": "list_tools",
  "tools": [
    "search_countries",
    "get_country_details"
  ]
}
```

### B. Tool 1: `search_countries` Invocation
**Request:**
`search_countries(query="turkey", limit=2)`

**Response:**
```json
[
  {
    "name": "Türkiye",
    "capital": "Ankara",
    "region": "Asia",
    "population": null
  }
]
```

### C. Tool 2: `get_country_details` Invocation
**Request:**
`get_country_details(name="Germany")`

**Response:**
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

### D. Edge-Case / Error Scenarios Tested
1. **Empty Query in `search_countries`:**
   - Input: `query=""`
   - Response: `[{"error": "query must not be empty"}]`
2. **Invalid Country in `get_country_details`:**
   - Input: `name="AtlantisCity99"`
   - Response: `{"error": "No country found matching 'AtlantisCity99'"}`

---

## 3. Error Handling & Hardening Strategy
To guarantee server stability and adhere to the MCP contract (never crashing the STDIO loop), several defensive mechanisms were implemented:
1. **Input Validation:** Non-string types, blank strings, and whitespace inputs are trapped immediately before issuing network calls, returning clean diagnostic error dictionaries.
2. **Graceful Upstream Handling & Fallbacks:** REST Countries endpoints can suffer from network timeouts, deprecation changes, or connection drops. Both tools wrap HTTP calls inside `try...except (httpx.HTTPError, httpx.TimeoutException)` blocks with tight timeouts. If upstream requests fail or return non-list structures, the server seamlessly falls back to a bundled country data snapshot without raising unhandled exceptions.
3. **Structured Non-Fatal Error Objects:** Instead of terminating the server process or emitting unparsed stack traces across STDIO, tools return structured JSON error payloads (`{"error": "..."}`) which LLM agents can easily parse and self-correct from.

---

## 4. What I Learned (Controlling Agent Context Reach)
MCP servers fundamentally shift how agents interact with external information by turning arbitrary APIs into strongly-typed, schema-bounded capabilities. Rather than dumping entire web payloads or full databases into an agent's context window (which inflates token consumption and degrades reasoning precision), an MCP server acts as an intelligent context filter. By carefully defining concise return shapes and defensive error messages, the server ensures the agent receives only dense, highly relevant domain facts. Designing tools with predictable structure and graceful failure paths allows autonomous agents to explore data environments safely and reliably without breaking the execution loop.
