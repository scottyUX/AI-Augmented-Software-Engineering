# Week 5 — Data Explorer MCP Server: Writeup

## Setup

- **MCP client:** GitHub Copilot agent mode in VS Code (GitHub Codespaces). Registered with
  `.vscode/mcp.json`:
  ```json
  { "servers": { "data-explorer": { "type": "stdio", "command": "python",
      "args": ["${workspaceFolder}/assignments/05-advanced-context-management/work/server.py"] } } }
  ```
  (The README also shows the equivalent Antigravity / Claude Desktop config.)
- **Transport:** STDIO.
- **Two problems with the starter, found while getting it to run:**
  1. **REST Countries v3.1 has been retired.** Every `restcountries.com/v3.1/...` URL now
     answers `301` → a JSON error *"This API version has been deprecated … migrate to our new
     version (v5)"*. The first run of my server returned `bad_response` for every query
     because of this (the error handling worked, the data source didn't). v5
     (`api.restcountries.com/countries/v5`) answers `401 authKeyMissing` without a key.
     So the server uses v5 when `RESTCOUNTRIES_API_KEY` is set, and otherwise the open
     `mledoze/countries` dataset (the data REST Countries was built on), downloaded once
     and searched locally. Both are mapped to the same output shape.
  2. **mcp 2.x removed `mcp.server.fastmcp`**, so an unpinned install fails on import.
     `requirements.txt` pins `mcp>=1.2,<2`.

## Transcript — an agent calling both tools

The full exported chat (exact tool inputs and outputs) is in
[`agent_transcript.md`](agent_transcript.md). Summary:

| # | Prompt | Tool call the agent made | Result |
|---|---|---|---|
| 1 | Find countries matching "guinea", then Jordan's currencies, languages, neighbors and flag | `search_countries {"query": "guinea", "limit": 10}` | Guinea, Guinea-Bissau, Equatorial Guinea, Papua New Guinea |
| | | `get_country_details {"name": "Jordan"}` | JOD / د.ا, Arabic, borders IRQ ISR PSE SAU SYR, `flagcdn.com/w320/jo.png` |
| 2 | Call `get_country_details` with "12345", then "Atlantis" | `get_country_details {"name": "12345"}` | `{"error": "name may only contain letters, spaces and . ' - ( ) , &", "error_type": "invalid_input"}` |
| | | `get_country_details {"name": "Atlantis"}` | `{"error": "no country found matching 'Atlantis'; try search_countries to find the exact name", "error_type": "not_found"}` |

The agent picked `search_countries` vs `get_country_details` from the tool descriptions alone,
and passed the structured errors back to the user unchanged.

A second, scripted MCP client (`mcp.ClientSession` over STDIO) also exercised edge cases:
`"Niger"` → Niger with `"other_matches": ["Nigeria"]`; `"   "` → `invalid_input`;
`limit: 99` → `invalid_input`.

## How I handled errors

Both tools **never raise**. Every failure becomes `{"error": <message>, "error_type": <kind>}`,
so the agent can read what went wrong and decide what to do next (fix the input, retry
later, or call `search_countries` first). One helper, `_http_get_json`, owns all HTTP handling.

| Failure | Handling |
|---|---|
| Empty / whitespace / wrong type / >100 chars / digits or symbols | `invalid_input`, rejected **before** any network call (a test checks no request is made) |
| `limit` outside 1–25, or a bool/string | `invalid_input` |
| Real names with punctuation or other scripts (`Côte d'Ivoire`, `Congo (Kinshasa)`, `الأردن`) | accepted |
| No match | `search_countries` → `[]`; `get_country_details` → `not_found` with a hint |
| Timeout (10 s) | `timeout` |
| DNS / connection error | `network` (a failed dataset download is not cached, so the next call retries) |
| 401 / 403 | `auth` ("check RESTCOUNTRIES_API_KEY") |
| 429 | `rate_limited` |
| Other 4xx / 5xx | `upstream_http` with the status code |
| Non-JSON or unexpected shape (e.g. the v3.1 deprecation envelope) | `bad_response` |
| Missing fields (e.g. no currency) | empty lists / `null`, never a `KeyError` |

Ambiguous names are ranked: exact common/official name, then exact alternate spelling, then
prefix match. That way `"Niger"` returns Niger, not Nigeria, and lists the others in
`other_matches`.

**Tests:** `test_server.py` has 38 cases with HTTP faked by `monkeypatch`, covering both data
sources and every row above. `pytest -q` → **38 passed**.

## What I learned

An MCP server decides exactly what context an agent can reach and in what shape. Returning
a small, fixed set of fields instead of the raw API payload (a single v5 country object is
tens of kilobytes) keeps the agent's context window focused on what the task needs.
Structured errors matter as much as results, because the error text is what the model
reasons over next: *"not found, try search_countries"* steers the agent better than a stack
trace. Validating input before any network call is also a safety boundary, since the model
can't use the tool to reach arbitrary URLs. Finally, an external API is a dependency that
can change under you, as REST Countries v3.1 did. Hiding the data source behind a stable tool
contract let me switch sources without changing anything the agent sees.
