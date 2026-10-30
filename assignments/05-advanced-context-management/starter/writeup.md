# Week 5 Writeup — Build a Custom MCP Server: The Data Explorer

**Student:** Zuhal Çolak  
**Agent / MCP Client:** Antigravity / Gemini CLI  
**Server Implementation:** `FastMCP` over STDIO  
**Data Source:** Open `mledoze/countries` dataset (the source data behind REST Countries)  
**Test Suite:** 22/22 unit and integration tests passing offline (`pytest`)  

---

## 1. Agent Tool Invocation Transcript

The `data-explorer` MCP server was registered via STDIO in the agent environment. The AI agent was prompted to plan a travel summary and currency lookup for Germany and Turkey, and to test boundary and error conditions using the MCP tools.

Below is the verified invocation transcript showing arguments, tool calls, and structured outputs:

### Step 1: Discovering Countries with `search_countries`
**User Prompt:**  
> *"Search for countries in Europe matching 'germ' and find out their capitals and regions."*

**Agent Tool Call:**
```json
{
  "name": "search_countries",
  "arguments": {
    "query": "germ",
    "limit": 5
  }
}
```

**MCP Server Response:**
```json
[
  {
    "name": "Germany",
    "capital": "Berlin",
    "region": "Europe",
    "subregion": "Western Europe"
  }
]
```

---

### Step 2: Retrieving Full Details with `get_country_details`
**User Prompt:**  
> *"Get detailed information for 'Turkey', including its official name, currency, languages, borders, and flag."*

**Agent Tool Call:**
```json
{
  "name": "get_country_details",
  "arguments": {
    "name": "Turkey"
  }
}
```

**MCP Server Response:**
```json
{
  "name": "Türkiye",
  "official_name": "Republic of Turkey",
  "cca2": "TR",
  "cca3": "TUR",
  "currencies": {
    "TRY": {
      "name": "Turkish lira",
      "symbol": "₺"
    }
  },
  "languages": {
    "tur": "Turkish"
  },
  "borders": [
    "ARM",
    "AZE",
    "BGR",
    "GEO",
    "GRC",
    "IRN",
    "IRQ",
    "SYR"
  ],
  "flag_url": "https://raw.githubusercontent.com/mledoze/countries/master/data/tur.svg"
}
```
*Note: The server resolved the historical English spelling "Turkey" to the dataset's native common name "Türkiye" via `altSpellings`, and normalized the flag URL to lower-case `tur.svg`.*

---

### Step 3: Handling Ambiguous Queries
**User Prompt:**  
> *"Look up details for 'Dominic'."*

**Agent Tool Call:**
```json
{
  "name": "get_country_details",
  "arguments": {
    "name": "Dominic"
  }
}
```

**MCP Server Response:**
```json
{
  "error": "ambiguous country name 'Dominic', multiple matches found",
  "candidates": [
    "Dominica",
    "Dominican Republic"
  ]
}
```
**Agent Follow-up:**  
The agent parsed the candidate list, recognized that the user might mean either Dominica or the Dominican Republic, and politely asked the user to disambiguate.

---

### Step 4: Handling Non-Existent Input
**User Prompt:**  
> *"Look up the country 'Atlantis'."*

**Agent Tool Call:**
```json
{
  "name": "get_country_details",
  "arguments": {
    "name": "Atlantis"
  }
}
```

**MCP Server Response:**
```json
{
  "error": "country 'Atlantis' not found"
}
```

---

### Step 5: Handling Empty / Malformed Input
**Agent Tool Call:**
```json
{
  "name": "search_countries",
  "arguments": {
    "query": "   ",
    "limit": -1
  }
}
```

**MCP Server Response:**
```json
[
  {
    "error": "query must be a non-empty string"
  }
]
```

---

### Step 6: Handling Simulated Upstream Timeout
**Simulated Event:** Upstream network timeout when fetching dataset.  
**MCP Server Response:**
```json
{
  "error": "upstream request timed out",
  "retryable": true
}
```
**Agent Action:** Because `retryable` is `true`, the agent informed the user that the external data source was temporarily unavailable and suggested retrying shortly without hallucinating country data.

---

## 2. Error Handling Approach

To ensure the server never crashes or hangs the agent:
1. **Type & Bounds Validation**: Both tools check argument types and values before processing. Empty strings, whitespace-only queries, non-strings, and non-positive limit integers immediately return structured error payloads without making downstream calls.
2. **Predictable Schema Shapes**: Errors return as clean JSON dictionaries containing an `"error"` message and, where relevant, a `"retryable": true` flag or a `"candidates"` list. The server never raises unhandled exceptions to STDIO.
3. **Smart Matching & Normalization**: Diacritics and casing are normalized using Unicode NFKD decomposition (`normalize_text`). Lookups check common names, official names, ISO codes (`cca2`, `cca3`, `cioc`), and `altSpellings` so common inputs like "Turkey", "DEU", or "UK" resolve smoothly.
4. **Resilient In-Memory Caching**: The dataset is downloaded on the first request and cached in `_countries`. Crucially, if the initial download throws an `httpx.TimeoutException` or `httpx.HTTPError`, the cache remains `None`. This guarantees that transient network errors do not permanently break the server.
5. **Asset URL Normalization**: The upstream repository stores SVG flags with lower-case filenames (`data/{cca3}.svg`). Casing is explicitly lower-cased (`cca3.lower()`) to prevent 404 image errors.

---

## 3. Reflection: Controlling What Context an Agent Can Reach

Building a custom MCP server highlights that an agent's reasoning power is directly bounded by the precision and structure of the context it can access. Exposing focused tools rather than raw, uncurated data dumps prevents context window saturation and drastically lowers hallucination rates. Furthermore, providing typed schemas, normalized outputs, and deterministic error messages allows the model to act as a resilient operator that can detect ambiguities and recover from upstream failures. Ultimately, the Model Context Protocol transforms probabilistic language models into reliable software systems by enforcing clean architectural boundaries between agent reasoning and external ground truth.
