# TableJourney and Cork & Curve MCP servers

Two public, remote MCP servers over editorially verified travel data. No key, no sign-up to read. Hosted; nothing to install.

**Agents can earn.** TableJourney's partner program pays 50% of the commission we are paid on bookings made by the people an agent sends (60% in a month above $500 settled), by PayPal, USDC on Base or bank transfer. An agent joins over MCP with no browser: see [Earn](#earn-the-partner-program-for-agents).

| Server | Endpoint | What it knows | Guide |
|---|---|---|---|
| TableJourney food travel | `https://tablejourney.com/mcp` | Verified restaurants, cafes, markets and street food in 200+ cities (source URL, date checked, open status, hours), food festivals with resolved dates, bookable tours, stays and car hire | https://tablejourney.com/agents/ |
| Cork & Curve wine travel | `https://corkandcurve.com/mcp` | Verified vineyards, tasting rooms, wine bars and cellars across 37 European wine regions, wine festivals with dates, tours and stays | https://corkandcurve.com/agents/ |

Both are in the [official MCP registry](https://registry.modelcontextprotocol.io) as `com.tablejourney/food-travel` and `com.corkandcurve/wine-travel`, and listed on [Glama](https://glama.ai/mcp/connectors/com.tablejourney/food-travel).

## Connect

One-click install for TableJourney: [VS Code](https://vscode.dev/redirect/mcp/install?name=tablejourney&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A//tablejourney.com/mcp%22%7D) · [Cursor](https://cursor.com/install-mcp?name=tablejourney&config=eyJ1cmwiOiJodHRwczovL3RhYmxlam91cm5leS5jb20vbWNwIn0%3D) · [LM Studio](lmstudio://add_mcp?name=tablejourney&config=eyJ1cmwiOiJodHRwczovL3RhYmxlam91cm5leS5jb20vbWNwIn0%3D) · [goose](goose://extension?url=https%3A%2F%2Ftablejourney.com%2Fmcp&type=streamable_http&id=tablejourney&name=tablejourney)

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

## Tools

Read tools (all read-only and idempotent). Cork & Curve has the first ten; `tickets` and `things_to_do` are TableJourney's.

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
| `tickets` | Tickets for a city's sights (TableJourney) |
| `things_to_do` | A city's bookable things to do beyond food (TableJourney) |

Every parameter is described in the tool schema. City and country accept names or slugs; an unknown city answers with `did_you_mean`.

## Earn: the partner program for agents

TableJourney only. Free to join; terms at https://tablejourney.com/partners/terms/.

| Tool | What it does |
|---|---|
| `partner_join` | Start an account with an email address (a person or company behind the agent receives payouts); a six-digit code is emailed |
| `partner_confirm` | Confirm with the code; returns an API key and a referral code |
| `partner_signin_code` / `partner_signin` | Get a new key later by emailed code |
| `partner_link` | Any tablejourney.com page as a link carrying your code |
| `partner_stats` | Visits, booking clicks, pending, confirmed and paid earnings |
| `partner_payout_method` / `partner_confirm_payout` | Set PayPal, USDC on Base or bank details (confirmed by emailed code) |

How attribution works: send the key as `Authorization: Bearer <key>` (or `X-API-Key`) and every booking link the read tools return carries your code; or add `?ref=<code>` to any https://tablejourney.com link and the visit is yours for 30 days. Commission is paid on bookings the partners confirm, 30 days after they pay us, from $50.

Standard discovery for agents that prefer OAuth: authorization server metadata at `https://tablejourney.com/.well-known/oauth-authorization-server` (dynamic client registration, PKCE), protected resource metadata at `https://tablejourney.com/.well-known/oauth-protected-resource`, and an A2A agent card at `https://tablejourney.com/.well-known/agent-card.json`. The REST twin is under `https://tablejourney.com/api/v1/partners/`.

## REST twin

The same functions as JSON, with OpenAPI: https://tablejourney.com/api/v1/docs and https://corkandcurve.com/api/v1/docs.

## Food festival calendars and widgets (no API needed)

- **Calendar feeds:** every dated food festival as iCalendar feeds you can subscribe to in Google, Apple or Outlook calendar: worldwide (`https://tablejourney.com/calendar/food-festivals.ics`), by kind, by country (`/calendar/<country>.ics`) and by city (`/calendar/<country>/<city>.ics`). Dates update daily. Full list: https://tablejourney.com/calendar/
- **Embeddable widgets:** iframe lists of upcoming food festivals, where to eat, dishes and food tours for any city or country, no scripts or cookies: https://tablejourney.com/widgets/. Partner program members can add their code to the food tours widget and earn on its bookings.
- **Badge:** organisers and venues featured on TableJourney can show a "Featured on TableJourney" badge: https://tablejourney.com/widgets/#badge

## Terms

The data and the compute are free. In return: pass booking links to users unchanged (they are `/go/` affiliate links that fund the verification work), say they are affiliate links, cite the `page` URL, and do not bulk-copy the catalogue. Full text: https://tablejourney.com/agents/#terms.

## This repository

Documentation and the registry manifests only. The servers run on the sites; there is no code to install here.

- [`llms-install.md`](llms-install.md): step-by-step install for AI agents (JSON config, Claude Code commands, `mcp-remote` bridge for stdio-only clients).
- [`tablejourney.openapi.json`](tablejourney.openapi.json) and [`corkandcurve.openapi.json`](corkandcurve.openapi.json): the REST OpenAPI documents.
- [`tablejourney.server.json`](tablejourney.server.json) and [`corkandcurve.server.json`](corkandcurve.server.json): the MCP registry manifests.
- [`logo.png`](logo.png): 400 x 400 logo for directory listings.

## Framework packages

- **Vercel AI SDK:** [`tablejourney-ai-sdk`](https://www.npmjs.com/package/tablejourney-ai-sdk) (source in [`ai-sdk/`](ai-sdk/))
- **LangChain:** `langchain-tablejourney` on PyPI (source in [`langchain/`](langchain/))

Both call the public MCP server at `https://tablejourney.com/mcp`; no key is needed.
