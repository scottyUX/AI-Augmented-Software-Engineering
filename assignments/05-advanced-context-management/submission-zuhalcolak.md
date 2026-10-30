# Week 5 Submission (Build a Custom MCP Server: The Data Explorer) - Zuhal Çolak

**Repository:** https://github.com/zuhalcolak/week5-custom-mcp-server

Implemented the **Data Explorer MCP Server** using `FastMCP` over STDIO, wrapping the open `mledoze/countries` dataset.

### Completed Deliverables:
- **`server.py`**:
  - `search_countries(query, limit=5)`: Case- and accent-insensitive search with limit validation and structured error handling.
  - `get_country_details(name)`: Deep country lookup returning currencies, languages, borders, and flag URL (normalized to lower-case SVG assets).
  - Smart multi-field resolution matching common name, official name, ISO codes (CCA2, CCA3, CIOC), and alternative spellings (e.g., "Turkey" -> "Türkiye", "UK" -> "United Kingdom").
  - Non-cached transient failures for seamless recovery from network drops.
- **`README.md`**:
  - Installation, STDIO execution instructions, and MCP client registration guide (Antigravity/Gemini CLI, Claude Desktop).
  - Detailed tool reference documenting parameters, types, example inputs/outputs, and error responses.
- **`writeup.md`**:
  - Live AI agent invocation transcript covering both tools, ambiguous queries, not-found inputs, malformed parameters, and upstream timeouts.
  - Detailed error-handling documentation.
  - 3–5 sentence reflection on controlling agent context boundaries.
- **Test Suite (`tests/test_server.py`)**:
  - 22 comprehensive unit and integration tests passing offline with `pytest`.
