# Data Explorer — MCP Server

An MCP server (STDIO transport) that exposes country data to an agent as two tools.

## Data source (important)

The starter targeted REST Countries **v3.1** (`restcountries.com/v3.1/...`). That API has
been **retired**: every v3.1 URL now 301-redirects to a JSON error saying
*"This API version has been deprecated … migrate to our new version (v5)"*, so the
starter's `search_countries` fails. The current API, **v5** (`api.restcountries.com/countries/v5`),
needs a free key. The server therefore picks a source at runtime:

| `RESTCOUNTRIES_API_KEY` | Source | Notes |
|---|---|---|
| set | REST Countries v5 (`?q=<name>`, `Authorization: Bearer <key>`) | free plan: 1,000 req/month, 20 req/10 s |
| not set | open [`mledoze/countries`](https://github.com/mledoze/countries) dataset (what REST Countries was built on), downloaded once and searched locally | `population` is `null` |

Both are mapped to the same output shape; `get_country_details` reports which one it used in `source`.
Get a key at https://restcountries.com/sign-up and **never commit it** — pass it through the
environment (see the client config below).

## Install

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

> `mcp` is pinned to `<2`: version 2.x renamed `FastMCP` to `MCPServer`, so the
> 1.x import `from mcp.server.fastmcp import FastMCP` fails on a fresh unpinned install.

## Run

```bash
python server.py        # speaks MCP over STDIO; it waits silently for a client
pytest -q               # 38 offline tests (HTTP is faked), no network needed
```

Try it interactively with the MCP Inspector (needs Node.js):

```bash
npx @modelcontextprotocol/inspector python server.py
```

## Register in an MCP client

Use **absolute paths**, and point `command` at the Python inside your venv so the
client finds `mcp` and `httpx`.

**Antigravity** — Agent panel → `…` → *MCP Servers* → *Manage MCP Servers* → *View raw config*
(`mcp_config.json`):

```json
{
  "mcpServers": {
    "data-explorer": {
      "command": "/absolute/path/to/starter/.venv/bin/python",
      "args": ["/absolute/path/to/starter/server.py"],
      "env": { "RESTCOUNTRIES_API_KEY": "<your key, optional>" }
    }
  }
}
```

**Claude Desktop** — Settings → Developer → Edit Config (`claude_desktop_config.json`), same
`mcpServers` block. **VS Code** uses `.vscode/mcp.json` with a top-level `"servers"` key
instead of `"mcpServers"`.

On Windows the Python path looks like `C:\\path\\to\\starter\\.venv\\Scripts\\python.exe`.

## Tool reference

### `search_countries(query: str, limit: int = 5) -> list[dict]`

Find countries by full or partial name.

| Parameter | Type | Rules |
|---|---|---|
| `query` | string | 1–100 chars; letters, spaces and `. ' - ( ) , &` only |
| `limit` | int | 1–25, default 5 |

```jsonc
// input
{"query": "jor", "limit": 2}
// output
[{"name": "Jordan", "capital": "Amman", "region": "Asia", "population": null}]
// population is a number when RESTCOUNTRIES_API_KEY is set (v5)
// no match -> []
```

### `get_country_details(name: str) -> dict`

Details for one country. Results are ranked so an exact common/official name wins
(so `Niger` doesn't return `Nigeria`), then exact alternate names, then prefix matches.

| Parameter | Type | Rules |
|---|---|---|
| `name` | string | same rules as `query` |

```jsonc
// input
{"name": "Jordan"}
// output
{
  "name": "Jordan",
  "official_name": "Hashemite Kingdom of Jordan",
  "capital": "Amman",
  "region": "Asia",
  "currencies": [{"code": "JOD", "name": "Jordanian dinar", "symbol": "د.ا"}],
  "languages": ["Arabic"],
  "borders": ["IRQ", "ISR", "PSE", "SAU", "SYR"],
  "flag_url": "https://flagcdn.com/w320/jo.png",
  "flag_emoji": "🇯🇴",
  "source": "mledoze/countries (no API key set)"
}
```

When a partial name matches several countries, the result also has
`"other_matches": [...]` (up to 5 names).

### Errors (both tools)

Tools never raise. Failures come back as
`{"error": "<human-readable message>", "error_type": "<kind>"}`
(`search_countries` wraps it in a one-item list).

| `error_type` | When |
|---|---|
| `invalid_input` | empty, too long, wrong type, or illegal characters; `limit` out of range (no network call is made) |
| `auth` | v5 rejected the key (401/403) |
| `rate_limited` | v5 returned 429 |
| `not_found` | `get_country_details` found no country |
| `timeout` | no answer within 10 s |
| `network` | DNS / connection failure |
| `upstream_http` | any other 4xx/5xx (e.g. 500) |
| `bad_response` | API returned non-JSON or an unexpected shape |
