# Week 4 Writeup — Data Explorer MCP Server

**Name:** Parwana Babakarkhil
**Client:** Google Antigravity (Gemini 3.8 Flash), Windows 11
**Transport:** STDIO

## Transcript: an agent calling both tools

The full transcript with the exact arguments and raw MCP results is in
[`transcript.md`](transcript.md). In one Antigravity conversation I asked the agent to use
only the `data-explorer` tools and make these five calls:

| # | Tool | Arguments | Result |
|---|---|---|---|
| 1 | `search_countries` | `{"query": "united", "limit": 3}` | United Arab Emirates, United Kingdom, Mexico |
| 2 | `get_country_details` | `{"name": "Japan"}` | JPY (¥), Japanese, no borders, flag URL |
| 3 | `get_country_details` | `{"name": "Türkiye"}` | currency, language, neighbours and flag (see transcript) |
| 4 | `get_country_details` | `{"name": "zzzz"}` | `{"error": "no country found matching 'zzzz'"}` |
| 5 | `search_countries` | `{"query": ""}` | `[{"error": "query must not be empty"}]` |

The results came back in MCP format (`content` + `structuredContent`, `isError: false`),
which shows the agent called the tools through the server, not through its own knowledge.
Calls 4 and 5 show bad input returning a clean message instead of crashing the server.

## How I handled errors

- **Input validation first:** empty or whitespace-only input, text over 100 characters, and
  a `limit` outside 1–25 (including booleans) are rejected before any network call.
- **One shared loader:** all network access goes through `_load_countries()`, which turns
  every failure into a `(None, message)` pair: timeouts (`httpx.TimeoutException`),
  connection errors (`httpx.HTTPError`), HTTP status 400+, invalid JSON, and a response that
  is not a list. Both tools reuse it, so they handle errors the same way.
- **No results is not an error for search:** `search_countries` returns `[]`, while
  `get_country_details` returns `{"error": "no country found ..."}` because it promises one
  country.
- **Partial data:** missing fields (`capital`, `currencies`, `borders`) are read with safe
  defaults, so a country with incomplete data still returns a valid shape.
- **Caching:** the dataset is downloaded once and cached; a failed download is not cached,
  so the next call retries.

## Two real problems I hit

1. **`mcp` 2.x broke the starter.** `pip install mcp` installed 2.3.0, and
   `from mcp.server.fastmcp import FastMCP` failed with *"This is mcp 2.x, where FastMCP was
   renamed to MCPServer"*. I pinned `mcp<2` in `requirements.txt`.
2. **REST Countries v3.1 is deprecated.** Every request got a redirect, and the redirected
   response was an error object ("This API version has been deprecated."). My error
   handling returned *"the countries API returned a response that is not valid JSON"*
   instead of crashing, which is how I noticed. Because v5 needs an API key, I switched to
   the open `mledoze/countries` dataset that REST Countries was built on. The trade-off: it
   has no population field, so `search_countries` returns `subregion` instead.

## What I learned

An MCP server decides exactly what context an agent can reach: the agent sees only the
tools I expose, their parameters, and the shape of what they return, so the tool
description and return format matter as much as the code. Returning small, structured
results (a few named fields instead of the full API record) keeps the agent's context short
and makes it easier for the model to use the answer. Clean error messages are part of that
context too: when the tool says "query must not be empty", the agent can fix its own call
instead of failing silently. I also saw that an agent's reach depends on things outside my
code, like a deprecated API or a breaking library release, so pinning versions and
handling upstream failures are part of controlling what the agent can do.
