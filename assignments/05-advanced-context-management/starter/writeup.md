# MCP Server Implementation Writeup — Data Explorer

## Agent Interaction Transcript

### Tool Call 1: `search_countries`
- **Agent Input:**
  ```json
  { "query": "canada" }
  ```
- **Tool Response:**
  ```json
  [
    {
      "name": "Canada",
      "capital": "Ottawa",
      "region": "Americas",
      "subregion": "North America"
    }
  ]
  ```

---

### Tool Call 2: `get_country_details`
- **Agent Input:**
  ```json
  { "name": "Japan" }
  ```
- **Tool Response:**
  ```json
  {
    "name": "Japan",
    "currencies": {
      "JPY": { "name": "Japanese yen", "symbol": "¥" }
    },
    "languages": ["Japanese"],
    "borders": [],
    "flag_url": "[https://raw.githubusercontent.com/mledoze/countries/master/data/jpn.svg](https://raw.githubusercontent.com/mledoze/countries/master/data/jpn.svg)"
  }
  ```

---

### Tool Call 3: Error Handling Validation
- **Agent Input (Invalid Country Name):**
  ```json
  { "name": "NonExistentCountry123" }
  ```
- **Tool Response:**
  ```json
  { "error": "country 'NonExistentCountry123' not found" }
  ```

---

## Error Handling Approach
Both tools prevent server process crashes by enforcing explicit validation and exception handling boundaries:
1. **Input Validation:** Pre-strips whitespace and returns clean error objects (`{"error": "name must not be empty"}`) for empty inputs.
2. **HTTP & Upstream Resiliency:** Catches network failures (`httpx.HTTPError`) during dataset retrieval and returns structured diagnostic error objects.
3. **No-Result Fallbacks:** Handles missing data cleanly by returning an explicit `not found` error dictionary instead of raising an unhandled exception.

---

## Reflection
Building an MCP server demonstrates how structured tools give AI agents deterministic access to external data. By decoupling API execution from model prompts, agents obtain precise live context without risk of hallucination or context window overload. Standardizing tool contracts ensures resilient error boundaries, allowing LLMs to process diagnostic failure objects gracefully and self-correct during reasoning.