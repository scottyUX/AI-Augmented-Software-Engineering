# Week 5 Submission (Custom MCP Server — Data Explorer): Kaan Erk Toraman (220901564)

Repository: https://github.com/kaan-erk/week5-mcp-data-explorer

- `server.py`: FastMCP server over STDIO exposing `search_countries` and `get_country_details` (currencies, languages, borders, and flag SVG URL).
- Robust error handling: Both tools return structured errors for empty/whitespace input, invalid types, negative limits, upstream timeouts, HTTP errors, and unknown country names; the server never crashes (23 automated pytest tests).
- Normalizes SVG flag URLs to lowercase (`cca3.lower()`), resolving GitHub raw URL case sensitivity where uppercase paths return HTTP 404.
- Driven from an MCP client over STDIO; complete JSON-RPC 2.0 handshake and execution transcript in `transcript.txt` and `writeup.md`.
- `README.md` includes setup, STDIO execution, client registration (Antigravity, Claude Desktop, VS Code), and complete Tool Reference.
- Reflection on context control and agent boundary management in `writeup.md`.
