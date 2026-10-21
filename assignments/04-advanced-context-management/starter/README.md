# Data Explorer MCP Server

A Python-based Model Context Protocol (MCP) server developed using FastMCP and the REST Countries v5 API. The server exposes two tools for searching countries and retrieving detailed country information through STDIO transport.

## Setup

Install the required dependencies:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file must include `python-dotenv` because the server uses `load_dotenv()` to load the REST Countries API key from a local `.env` file. This keeps the API key separate from the source code instead of hardcoding it, improving security and configuration management.

Create a `.env` file in the `starter` directory:

```env
RESTCOUNTRIES_API_KEY=your_api_key_here
```

An API key can be obtained from [REST Countries](https://restcountries.com/).

**Security:** Keep the `.env` file private and ensure it is excluded from Git tracking.

## Run

Start the MCP server:

```bash
python server.py
```

The server communicates over STDIO and is intended to be launched by an MCP-compatible client.

## Register in an MCP Client

Configure your MCP client to launch the server using the Python interpreter from the environment where the dependencies are installed.

Example configuration:

```json
{
  "mcpServers": {
    "data-explorer": {
      "command": "/absolute/path/to/python",
      "args": ["/absolute/path/to/starter/server.py"],
      "cwd": "/absolute/path/to/starter"
    }
  }
}
```

Replace the example paths with the actual paths on your system. On Windows, use valid Windows paths and escape backslashes in JSON.

The server was tested using **MCP Inspector** with STDIO transport. Both tools were successfully invoked.

## Tool Reference

### 1. `search_countries`

Searches for countries by name and returns basic information about matching countries.

**Parameters:**

- `query` (string, required): Country name or search text.
- `limit` (integer, optional): Maximum number of results, between 1 and 20. Default: 5.

**Example input:**

```json
{
  "query": "Germany",
  "limit": 5
}
```

**Example output:**

```json
[
  {
    "name": "Germany",
    "capital": "Berlin",
    "region": "Europe",
    "population": 83298787
  }
]
```

If no matching countries are found, the tool returns an empty list.

### 2. `get_country_details`

Retrieves detailed information about a country, including its currencies, languages, bordering countries, and flag URL.

**Parameters:**

- `name` (string, required): Country name.

**Example input:**

```json
{
  "name": "Germany"
}
```

**Example output:**

```json
{
  "name": "Germany",
  "currencies": [
    {
      "code": "EUR",
      "name": "Euro",
      "symbol": "€"
    }
  ],
  "languages": [
    {
      "bcp47": "de",
      "iso639_1": "de",
      "iso639_2b": "ger",
      "iso639_2t": "deu",
      "iso639_3": "deu",
      "name": "German",
      "native_name": "Deutsch"
    }
  ],
  "borders": [
    "AUT",
    "BEL",
    "CZE",
    "DNK",
    "FRA",
    "LUX",
    "NLD",
    "POL",
    "CHE"
  ],
  "flag_url": "https://flags.restcountries.com/v5/w640/de.png"
}
```

## Error Handling

Both tools implement input validation and error handling to prevent unexpected failures.

The server handles:

- Empty or invalid input values
- Invalid result limits
- API request timeouts
- HTTP and connection errors
- Unexpected API response structures
- Countries that cannot be found

For example, an unknown country returns an empty list from `search_countries`, while `get_country_details` returns a structured `Country not found` error.

## Testing and Documentation

The MCP server was tested using MCP Inspector over STDIO. Both tools successfully retrieved country information for Germany.

Input validation, missing-country scenarios, simulated timeouts, and connection failures were also tested.

The detailed tool invocation transcript, error-handling results, and reflection are documented in `writeup.md`.
