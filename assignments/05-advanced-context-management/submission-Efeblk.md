# Week 5 Submission: Efeblk

Repository: https://github.com/Efeblk/week5-mcp-server

- FastMCP server over STDIO with `search_countries` and the new `get_country_details` (official name, capital, subregion, currencies, languages, borders, flag URL).
- Errors are returned as data and never crash the server: input validation, missing API key, timeouts, network errors, 401/403, 429, other HTTP errors, unexpected response shapes.
- REST Countries v3.1 was shut down during the assignment, so the server uses the v5 API (key read from `RESTCOUNTRIES_API_KEY`).
- Driven from two MCP clients: `client_demo.py` (good and bad input for both tools) and a Claude Code session that calls both tools to answer one question. Transcripts are in `outputs/` and `writeup.md`.
- README has install, run and register steps plus a tool reference.
- Tests: 18 pass, 1 skipped (live API test).
