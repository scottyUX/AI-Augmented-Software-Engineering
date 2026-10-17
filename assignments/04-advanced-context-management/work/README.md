# Data Explorer — MCP Server

A small [Model Context Protocol](https://modelcontextprotocol.io) server that gives an AI
agent two tools for looking up country data. It runs locally over **STDIO**.

> **Data source note:** the starter used the REST Countries **v3.1** API, which is now
> deprecated (every request is redirected to `"This API version has been deprecated."`),
> and the new v5 API requires an API key. To stay free and key-less, this server loads the
> open [`mledoze/countries`](https://github.com/mledoze/countries) dataset (the data REST
> Countries was built on) once, caches it in memory, and searches it locally. Flag images
> come from [flagcdn.com](https://flagcdn.com).

## Install

Requires Python 3.10+ (tested with Python 3.12 on Windows).

```bash
pip install -r requirements.txt
```

`requirements.txt` pins `mcp<2`: in `mcp` 2.x, `FastMCP` was renamed and
`from mcp.server.fastmcp import FastMCP` no longer works.

## Run

```bash
python server.py
```

The server speaks MCP over STDIO, so it waits silently for a client. You normally don't
run it by hand; the MCP client starts it.

## Register in an MCP client

Add this to the client's MCP config (use absolute paths for your machine).

**Google Antigravity** (`Customizations → Installed → MCP Servers → Copy Config File Path`,
then edit that `mcp_config.json`):

```json
{
  "mcpServers": {
    "data-explorer": {
      "command": "C:/Users/<you>/AppData/Local/Programs/Python/Python312/python.exe",
      "args": ["C:/Users/<you>/Documents/mcp-week4/server.py"]
    }
  }
}
```

The same block works for Claude Desktop (`claude_desktop_config.json`). Restart the client
after editing.

## Tool reference

### `search_countries(query, limit=5)`

Search countries by full or partial name (common name, official name, or alternative
spelling). Exact matches come first.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Full or partial country name, 1–100 characters. |
| `limit` | integer | no | Maximum results, 1–25 (default 5). |

**Returns:** a list of `{name, capital, region, subregion}`. An empty list means no match.

Example input: `{"query": "united", "limit": 3}`

```json
[
  {"name": "United Arab Emirates", "capital": "Abu Dhabi", "region": "Asia", "subregion": "Western Asia"},
  {"name": "United Kingdom", "capital": "London", "region": "Europe", "subregion": "Northern Europe"},
  {"name": "Mexico", "capital": "Mexico City", "region": "Americas", "subregion": "North America"}
]
```

(Mexico matches because its official name is "United Mexican States".)

### `get_country_details(name)`

Get details for one country. Prefers an exact name match ("Niger" never returns
"Nigeria"), otherwise uses the first partial match.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Country name, 1–100 characters, e.g. `"Japan"` or `"Türkiye"`. |

**Returns:** `{name, official_name, currencies, languages, borders, flag_url, flag_emoji}`.
`currencies` is a list of `{code, name, symbol}`; `borders` lists neighbouring country names
(empty for island nations).

Example input: `{"name": "Japan"}`

```json
{
  "name": "Japan",
  "official_name": "Japan",
  "currencies": [{"code": "JPY", "name": "Japanese yen", "symbol": "¥"}],
  "languages": ["Japanese"],
  "borders": [],
  "flag_url": "https://flagcdn.com/w320/jp.png",
  "flag_emoji": "🇯🇵"
}
```

### Errors

Both tools never raise; failures come back as structured messages
(`[{"error": "..."}]` for `search_countries`, `{"error": "..."}` for `get_country_details`):

| Situation | Example message |
|---|---|
| Empty / whitespace input | `query must not be empty` |
| Input too long | `name is too long (max 100 characters)` |
| Bad `limit` | `limit must be an integer between 1 and 25` |
| No match (details) | `no country found matching 'zzzz'` |
| Timeout | `the country data source did not respond within 10 seconds` |
| Network error | `could not reach the country data source: ConnectError` |
| HTTP error | `the country data source returned HTTP 500` |
| Invalid JSON / format | `the country data source returned a response that is not valid JSON` |
