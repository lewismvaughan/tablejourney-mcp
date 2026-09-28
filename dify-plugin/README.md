# TableJourney

Search verified food places, plan a food day, find festivals and bookable
food experiences across 200+ cities, straight from
[TableJourney](https://tablejourney.com)'s public agent API. No API key,
no account and no setup required.

## Tools

| Tool | Purpose |
|---|---|
| **Search verified places** (`search_places`) | Search verified restaurants, cafes, bakeries, markets and street food by text, city, cuisine, dietary need, price tier or distance from a point. |
| **Plan a food day** (`plan_day`) | Compose a one-day food itinerary for a city, slotted by time of day. |
| **Find food festivals** (`festivals`) | Find food festivals with resolved start and end dates. |
| **Find bookable experiences** (`experiences`) | Find bookable food tours, cooking classes and tickets from GetYourGuide, Viator or Musement. |
| **List cities** (`cities`) | List every city TableJourney covers, optionally by country, to find the exact slug for the other tools. |

Every place and festival result carries an address, an editorial score, a
short description, a page URL to cite, and a `provenance` block with the
source URL TableJourney used to verify the listing.

## Setup

1. Install this plugin from the Dify Marketplace.
2. Nothing else. TableJourney's API at `https://tablejourney.com/api/v1` is
   public and read-only; no credential is required to use any tool.
3. Optionally, open the TableJourney provider settings and paste an API
   key if you have one from [tablejourney.com/agents/](https://tablejourney.com/agents/).
   This only tags your requests for TableJourney's own attribution
   reporting; it does not unlock extra data, raise a rate limit, or change
   any tool's behavior. Leave it blank otherwise.

## How it works

Each tool calls one documented, fixed endpoint under
`https://tablejourney.com/api/v1` with a plain HTTPS GET request and
returns the JSON response. The full OpenAPI document is published at
[tablejourney.com/api/v1/openapi.json](https://tablejourney.com/api/v1/openapi.json).

* `GET /api/v1/places`
* `GET /api/v1/plan/{country}/{city}`
* `GET /api/v1/festivals`
* `GET /api/v1/experiences`
* `GET /api/v1/cities`

No command execution, code execution, SQL, filesystem access, browser
automation, or arbitrary user-controlled URL fetching is involved: every
request target is one of the five fixed paths above.

## Privacy

See [PRIVACY.md](./PRIVACY.md). Short version: the plugin sends only the
query parameters you or the calling LLM supply to `tablejourney.com`. It
stores nothing of its own.

## Source repository

[github.com/lewismvaughan/tablejourney-mcp/tree/main/dify-plugin](https://github.com/lewismvaughan/tablejourney-mcp/tree/main/dify-plugin)

TableJourney's own site and API are not a public source repository; the
API is documented at [tablejourney.com/agents/](https://tablejourney.com/agents/)
and its OpenAPI document is served at
[tablejourney.com/api/v1/openapi.json](https://tablejourney.com/api/v1/openapi.json).

## Contact

support@tablejourney.com. For security reports, follow Dify's
[security disclosure process](https://github.com/langgenius/dify-plugins#security-disclosure).

## License

MIT.
