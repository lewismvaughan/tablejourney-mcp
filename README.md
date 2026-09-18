# TableJourney and Cork & Curve MCP servers

Two public, read-only, remote MCP servers over editorially verified travel data. No key, no sign-up. Hosted; nothing to install.

| Server | Endpoint | What it knows | Guide |
|---|---|---|---|
| TableJourney food travel | `https://tablejourney.com/mcp` | Verified restaurants, cafes, markets and street food in 200+ cities (source URL, date checked, open status, hours), food festivals with resolved dates, bookable tours, stays and car hire | https://tablejourney.com/agents/ |
| Cork & Curve wine travel | `https://corkandcurve.com/mcp` | Verified vineyards, tasting rooms, wine bars and cellars across 37 European wine regions, wine festivals with dates, tours and stays | https://corkandcurve.com/agents/ |

Both are in the [official MCP registry](https://registry.modelcontextprotocol.io) as `com.tablejourney/food-travel` and `com.corkandcurve/wine-travel`, and listed on [Glama](https://glama.ai/mcp/connectors/com.tablejourney/food-travel).

## Connect

Claude Code:

```bash
claude mcp add --transport http tablejourney https://tablejourney.com/mcp
claude mcp add --transport http corkandcurve https://corkandcurve.com/mcp
```

Claude Desktop, Cursor, or any client that takes a JSON config:

```json
{
  "mcpServers": {
    "tablejourney": { "type": "streamable-http", "url": "https://tablejourney.com/mcp" },
    "corkandcurve": { "type": "streamable-http", "url": "https://corkandcurve.com/mcp" }
  }
}
```

Clients that only speak stdio can bridge with [`mcp-remote`](https://www.npmjs.com/package/mcp-remote): `npx mcp-remote https://tablejourney.com/mcp`.

## Tools (same ten on both servers)

| Tool | What it returns |
|---|---|
| `search_places` | Verified venues by text, city, kind, cuisine, dietary need, price tier, opening time (`open_at`) or near a coordinate |
| `place` | One venue in full by id, with `open_now_utc` and three nearby venues |
| `plan_day` | A composed day of open venues for a city, filtered by neighbourhood, dietary need, price tier and date |
| `festivals` | Festivals with their next resolved dates, by city, country, date window or text |
| `experiences` | Bookable tours, classes, tastings and tickets |
| `stays` | Hotels and stay partners with booking links |
| `car_hire` | Car hire partners that cover the city |
| `dishes` | Signature dishes (or wines) and where to find them |
| `itineraries` | Editorial day-by-day plans with every venue resolved |
| `cities` | Every city or region covered, with the slugs the other tools accept |

Every tool is read-only and idempotent; every parameter is described in the tool schema. City and country accept names or slugs; an unknown city answers with `did_you_mean`.

## REST twin

The same functions as JSON, with OpenAPI: https://tablejourney.com/api/v1/docs and https://corkandcurve.com/api/v1/docs.

## Terms

The data and the compute are free. In return: pass booking links to users unchanged (they are `/go/` affiliate links that fund the verification work), say they are affiliate links, cite the `page` URL, and do not bulk-copy the catalogue. Full text: https://tablejourney.com/agents/#terms.

## This repository

Documentation and the registry manifests only. The servers run on the sites; there is no code to install here.
