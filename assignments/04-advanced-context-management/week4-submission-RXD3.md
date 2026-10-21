# Week 4 — Data Explorer MCP Server Submission

**GitHub Username:** RXD3

**Assignment Repository:** https://github.com/RXD3/week4-mcp-data-explorer

## Overview

For this assignment, I built a custom MCP server using Python and FastMCP. It connects to the REST Countries API and provides two tools that Codex can use directly.

### Tools

- `search_countries(query, limit)` — Searches for countries and returns their names, capitals, regions, and populations.
- `get_country_details(name)` — Returns information about a country, including its currencies, languages, borders, and flag URL.

### Testing

I successfully connected the MCP server to the Codex extension in VS Code and tested both tools.

I also used Python's unittest library to test successful requests, invalid inputs, HTTP errors, timeouts, network failures, and malformed responses.

**Test Results:** 29 passed, 0 failed (reported by Codex).

The project repository includes the source code, tests, README documentation, and a writeup showing the actual MCP tool calls and what I learned.
