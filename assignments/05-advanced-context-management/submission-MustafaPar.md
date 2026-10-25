# Week 5 Submission (Advanced Context Management) — Mustafa Par

**Assignment:** Build a Custom MCP Server: The Data Explorer

**Repository:** https://github.com/MustafaPar/week4-mcp-data-explorer

> Submitted on 2026-10-15 as Week 4. The instructor has since swapped Weeks 4 and 5, so this
> assignment is now Week 5. The project is unchanged; its repository name and documents still
> say "Week 4" because they were written under the original schedule.

A `FastMCP` server over STDIO with two tools on the REST Countries API. The starter's v3.1 endpoint has been retired (every v1–v4 request now returns `301` to a deprecation notice), so the server uses v5 with a free API key, read from the `RESTCOUNTRIES_API_KEY` environment variable and never committed.

| Tool | Returns |
|---|---|
| `search_countries(query, limit=5)` | `{name, capital, region, population}` list (starter shape) |
| `get_country_details(name)` | currencies, languages, borders and flag URL, plus official name, ISO codes, capital, region, population and area |

Both tools validate input and return structured errors (`invalid_input`, `auth_failed`, `rate_limited`, `timeout`, `not_found`, `ambiguous`, ...) instead of crashing. 94 tests pass, using mocked HTTP plus in-memory and STDIO MCP sessions.

- [`README.md`](https://github.com/MustafaPar/week4-mcp-data-explorer/blob/main/README.md): install, run, register, and the tool reference with live example input and output.
- [`writeup.md`](https://github.com/MustafaPar/week4-mcp-data-explorer/blob/main/writeup.md): a live Claude Code transcript of both tools (including bad-input and ambiguous cases), how errors are handled, and what I learned about controlling what context an agent can reach.
