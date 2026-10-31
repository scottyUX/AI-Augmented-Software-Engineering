# Week 5 Writeup — Data Explorer MCP Server

## 1. Agent Transcript

```json
// 1. search_countries("germany", limit=1)
[
  {
    "name": "Germany",
    "capital": "Berlin",
    "region": "Europe",
    "subregion": "Western Europe"
  }
]

// 2. get_country_details("germany")
{
  "name": "Germany",
  "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
  "languages": {"deu": "German"},
  "borders": ["AUT", "BEL", "CZE", "DNK", "FRA", "LUX", "NLD", "POL", "CHE"],
  "flag": "https://raw.githubusercontent.com/mledoze/countries/master/data/deu.svg"
}

// 3. search_countries("") -> Bad Input
[{"error": "query must not be empty"}]

// 4. get_country_details("Atlantis") -> Not Found
{"error": "no country found for 'Atlantis'"}
```

## 2. Error Handling

Both tools validate inputs upfront, returning structured error objects (`[{"error": "..."}]` for `search_countries` and `{"error": "..."}` for `get_country_details`) when input strings are empty or whitespace. Network issues or failed upstream fetches are caught with `except httpx.HTTPError as exc:` and returned as `{"error": f"upstream request failed: {exc}"}` rather than raising uncaught exceptions, preventing server crashes over STDIO.

## 3. What I Learned

Controlling the context an agent can reach is critical to building reliable AI systems. Exposing targeted MCP tools rather than loading entire raw datasets prevents context window bloat and reduces model hallucination. Providing deterministic, structured return shapes and predictable error responses ensures that the agent can reliably interpret data and handle failures gracefully.
