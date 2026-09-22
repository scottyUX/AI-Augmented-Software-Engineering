# Week 4 — Build a Custom MCP Server: The Data Explorer

## Overview
Agents are only as good as the context they can reach. This week you'll extend an
agent's reach by building a **Model Context Protocol (MCP) server** that wraps a real
external API and exposes it as agent tools. This is the concrete, hands-on side of the
context-management lecture: you decide what context an agent can pull, in what shape,
and with what guardrails.

**New domain:** build a **"Data Explorer"** server over a *public, key-optional data
API* — not the productivity/notes integrations from typical examples.

## Learning goals
- Understand MCP building blocks: **tools, resources, prompts**, and **transport**.
- Implement typed tool definitions with real error handling.
- Follow transport best practices (no stdout noise on STDIO servers).
- Optionally implement authorization for HTTP transport.

---

## Requirements

1. **Choose a public API** with an interesting dataset. Suggested (pick one, or bring
   your own — must be different from the standard weather/GitHub/Notion examples):
   - **OpenLibrary** (books, authors, editions)
   - **TheMealDB** (recipes by ingredient/category)
   - **REST Countries** (country facts, borders, currencies)
   - **USGS Earthquakes** (recent quakes by region/magnitude)
   - **Open Trivia DB**, **TfL / transit**, **PokéAPI**, **Art Institute of Chicago**
   Document which endpoints you'll use.
2. **Expose at least two MCP tools** with typed parameters. Example for OpenLibrary:
   `search_books(query, limit)` and `get_book_details(work_id)`.
3. **Resilience:**
   - Graceful handling of HTTP errors, timeouts, and empty results.
   - Respect rate limits (simple backoff or a user-facing warning).
   - Validate inputs and return structured, model-friendly errors.
4. **Packaging & docs:** clear setup, env vars, and run commands, plus one example
   invocation flow (what to type in the client to trigger each tool).
5. **Pick a transport:**
   - **Local (STDIO):** runnable from your machine and discoverable by an MCP client
     (Claude Desktop, or an MCP-aware IDE).
   - **Remote (HTTP):** network-accessible and callable by an agent runtime.
     *Extra credit if deployed and reachable.*
6. **(Optional bonus) Auth:** API-key via env var, or OAuth2-style bearer tokens for
   HTTP transport with audience validation (never pass tokens through to the upstream API).

## Deliverables
- Source under `mcp-data-explorer/` with a clear entrypoint (`server/main.py` or similar).
- `README.md` with:
  - Prerequisites, env setup, and run instructions (local and/or remote).
  - How to register the server in an MCP client / agent runtime.
  - **Tool reference:** names, parameters, example inputs/outputs, expected behavior.
- A short `writeup.md`: which API and endpoints, your two+ tools, how you handled
  errors and rate limits, and one transcript of an agent using your tools.

## Evaluation (90 pts)
- **Functionality (35):** 2+ working tools, correct API integration, useful outputs.
- **Reliability (20):** input validation, error handling, logging, rate-limit awareness.
- **Developer experience (20):** clear docs, easy to run, sensible structure.
- **Code quality (15):** readable, typed, minimal complexity.
- **Extra credit (10):** +5 deployed remote HTTP server callable by an agent; +5 auth
  implemented correctly.

## References
- MCP server quickstart: https://modelcontextprotocol.io/quickstart/server
  *(you may not submit this example itself)*
- MCP authorization: https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization
- Remote MCP on Cloudflare Agents: https://developers.cloudflare.com/agents/guides/remote-mcp-server/
- Deploy MCP to Vercel (free tier): https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel
