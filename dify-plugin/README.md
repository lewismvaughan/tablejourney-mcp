# TableJourney

Food travel data from [TableJourney](https://tablejourney.com)'s public,
read-only agent API: verified places to eat and drink, food festivals with
dates, signature dishes, food itineraries, bookable food tours, tickets,
stays and car hire, across 224 cities. No API key, account or setup is
required.

## Tools

| Tool | Purpose |
|---|---|
| **Things to do in a city** (`things_to_do`) | Experiences, tickets and passes, food festivals in the trip window, places to eat, stays and car hire for one city in one answer. A good first call for trip planning. |
| **Search verified places** (`search_places`) | Restaurants, cafes, bakeries, markets, street food and bars by text, city, kind, cuisine, dietary need, price tier, opening time or distance from a point. |
| **Place details** (`place`) | One place by the id `search_places` returned, with whether it is open now and three places nearby. |
| **Plan a food day** (`plan_day`) | A one-day food plan for a city, slotted by time of day, every stop open on the given date. |
| **Food itineraries** (`itineraries`) | Ready-made day-by-day food itineraries for a city. |
| **Signature dishes** (`dishes`) | A city's signature dishes and the verified places that serve them. |
| **Find food festivals** (`festivals`) | Food festivals with resolved start and end dates, by country, city, date range or text. |
| **Find bookable experiences** (`experiences`) | Food tours, cooking classes and tastings from GetYourGuide, Viator or Musement. |
| **Where to stay** (`stays`) | Hotels and stay partners for a city. |
| **Tickets and passes** (`tickets`) | Ticket, city pass and tour partners covering a city. |
| **Car hire** (`car_hire`) | Car hire partners covering a city, with pick-up points where known. |
| **List cities** (`cities`) | Every covered city with its slug, optionally by country. |

City and country can be given as slugs (`new-york-city`, `italy`) or
names (`New York City`, `Italy`). An unknown city answers with suggestions.

Every place, dish and festival result carries a `page` URL on
tablejourney.com; the page has the address, opening hours, the sources the
listing was checked against and the date it was checked. Answers carry the
essentials (name, kind, cuisine, price tier, a one-line summary, festival
dates) and at most 20 results per call.

Booking links (`book`) are `https://tablejourney.com/go/` links that
forward to the booking partner. They are affiliate links; pass them to
users as returned.

## Setup

1. Install this plugin from the Dify Marketplace.
2. Dify asks you to authorize the TableJourney provider once (Tools,
   TableJourney, Authorize). Leave the key field blank and save; no
   credential is needed.
3. Optional: paste a TableJourney partner API key in that field instead
   ([tablejourney.com/agents/earn/](https://tablejourney.com/agents/earn/)).
   With a key, the booking links the tools return carry your partner code.
   The key does not change the data the tools return. An unrecognised key
   is reported when you save it.
4. Add any TableJourney tool to an agent, chatflow or workflow.

## Example

Ask an agent that has the TableJourney tools:

> I am in Lisbon from 14 to 16 November. What food festivals are on, which
> dishes should I try, and is there a good food tour?

A typical run calls `things_to_do` (country `portugal`, city `lisbon`,
`from` 2026-11-14, `to` 2026-11-16), then `dishes` for the same city.

## How it works

Each tool calls one fixed, documented endpoint under
`https://tablejourney.com/api/v1` with a plain HTTPS GET request (20 second
timeout) and returns the JSON answer plus a short text summary. The OpenAPI
document is at
[tablejourney.com/api/v1/openapi.json](https://tablejourney.com/api/v1/openapi.json).

* `GET /api/v1/things-to-do/{country}/{city}`
* `GET /api/v1/places` and `GET /api/v1/places/{country}/{city}/{kind}/{slug}`
* `GET /api/v1/plan/{country}/{city}`
* `GET /api/v1/itineraries/{country}/{city}`
* `GET /api/v1/dishes`
* `GET /api/v1/festivals`
* `GET /api/v1/experiences`
* `GET /api/v1/stays/{country}/{city}`
* `GET /api/v1/tickets/{country}/{city}`
* `GET /api/v1/cars/{country}/{city}`
* `GET /api/v1/cities`

No command execution, code execution, SQL, filesystem access, browser
automation, or arbitrary URL fetching is involved: every request goes to
one of the fixed paths above on tablejourney.com. The tools only read.

## Changes

* 0.0.2: seven new read-only tools (`things_to_do`, `dishes`,
  `itineraries`, `place`, `stays`, `tickets`, `car_hire`); city and country
  accept names as well as slugs; errors for an unknown city include
  suggestions; the optional key is described as the TableJourney partner
  key and is checked when saved; descriptions updated to what the API
  returns today. No breaking changes: the five tools from 0.0.1 keep their
  names and parameters.
* 0.0.1: first release (`search_places`, `plan_day`, `festivals`,
  `experiences`, `cities`).

## Privacy

See [PRIVACY.md](./PRIVACY.md). The plugin sends only the tool-call
parameters to `tablejourney.com` and stores nothing of its own.

## Source repository

[github.com/lewismvaughan/tablejourney-mcp/tree/main/dify-plugin](https://github.com/lewismvaughan/tablejourney-mcp/tree/main/dify-plugin)

The API is documented at
[tablejourney.com/agents/](https://tablejourney.com/agents/).

## Contact

support@tablejourney.com. For security reports, follow Dify's
[security disclosure process](https://github.com/langgenius/dify-plugins#security-disclosure).

## License

MIT.
