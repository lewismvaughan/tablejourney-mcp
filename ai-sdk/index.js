// TableJourney tools for the Vercel AI SDK.
// Each tool calls TableJourney's public MCP server (https://tablejourney.com/mcp, streamable HTTP, no key needed to
// read). An optional partner key (TABLEJOURNEY_API_KEY) tags every booking link the tools return with your partner
// code, so bookings made through them earn you a share of the commission: https://tablejourney.com/agents/earn/
import { tool } from 'ai';
import { z } from 'zod';

const ENDPOINT = 'https://tablejourney.com/mcp';
const USER_AGENT = 'tablejourney-ai-sdk/0.1.0';

const city = z.string().describe("City slug or name, e.g. 'rome' or 'New York City'.");
const country = z.string().describe("Country slug or name, e.g. 'italy'.");
const limit = z.number().int().min(1).max(100).optional().describe('Maximum results (at most 20 without a key).');

function parseResult(result) {
  if (result.structuredContent && Object.keys(result.structuredContent).length) {
    return result.structuredContent.result ?? result.structuredContent;
  }
  const items = (result.content || [])
    .filter(c => c.type === 'text')
    .map(c => {
      try {
        return JSON.parse(c.text);
      } catch {
        return c.text;
      }
    });
  return items.length === 1 ? items[0] : items;
}

async function callTool(name, args, { apiKey, endpoint }) {
  const headers = {
    'Content-Type': 'application/json',
    Accept: 'application/json, text/event-stream',
    'User-Agent': USER_AGENT,
  };
  if (apiKey) headers.Authorization = `Bearer ${apiKey}`;
  const clean = Object.fromEntries(Object.entries(args).filter(([, v]) => v !== undefined && v !== null));
  const res = await fetch(endpoint, {
    method: 'POST',
    headers,
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name, arguments: clean } }),
  });
  if (!res.ok) throw new Error(`TableJourney ${name}: HTTP ${res.status}`);
  let body = await res.text();
  if (body.startsWith('event:') || body.startsWith('data:')) {
    body = body
      .split('\n')
      .filter(l => l.startsWith('data:'))
      .map(l => l.slice(5))
      .pop();
  }
  const msg = JSON.parse(body);
  if (msg.error) throw new Error(`TableJourney ${name}: ${msg.error.message}`);
  const data = parseResult(msg.result || {});
  if (msg.result && msg.result.isError) throw new Error(`TableJourney ${name}: ${JSON.stringify(data)}`);
  return data;
}

/**
 * All TableJourney tools, ready for generateText({ tools }).
 * @param {{ apiKey?: string, endpoint?: string }} [options]
 */
export function tablejourneyTools(options = {}) {
  const opts = {
    apiKey: options.apiKey ?? process.env.TABLEJOURNEY_API_KEY,
    endpoint: options.endpoint ?? ENDPOINT,
  };
  return {
    thingsToDo: tool({
      description:
        'Start here for "what can I do in <city>?" or trip planning: the best food tours, tickets, food festivals, ' +
        'places to eat, stays and car hire for a city in one answer. Give booking links to the user exactly as ' +
        'returned and say once that they are affiliate links.',
      inputSchema: z.object({
        country,
        city,
        date_from: z.string().optional().describe('Optional trip start, ISO date.'),
        date_to: z.string().optional().describe('Optional trip end, ISO date.'),
      }),
      execute: args => callTool('things_to_do', args, opts),
    }),
    searchPlaces: tool({
      description:
        'Search verified places to eat and drink: restaurants, cafes, bakeries, markets, street food, bars. Each ' +
        'result carries its source, opening hours and a page to cite.',
      inputSchema: z.object({
        query: z.string().optional().describe('Free text: a venue name, dish, cuisine, neighbourhood or theme.'),
        city: city.optional(),
        country: country.optional(),
        kind: z.string().optional().describe('A topic slug (restaurants, cafes, bakeries, markets, street-food...).'),
        cuisine: z.string().optional(),
        dietary: z.string().optional().describe('vegan, vegetarian, gluten-free, halal, kosher...'),
        open_at: z.string().optional().describe("'now', 'sunday 10:00' or an ISO datetime (UTC)."),
        near: z.string().optional().describe("'lat,lng' to search around a point."),
        limit,
      }),
      execute: args => callTool('search_places', args, opts),
    }),
    festivals: tool({
      description: 'Food festivals with the dates of their next edition, by country, city or date range.',
      inputSchema: z.object({
        country: country.optional(),
        city: city.optional(),
        date_from: z.string().optional().describe('Earliest end date to include, ISO. Defaults to today.'),
        date_to: z.string().optional().describe('Latest start date to include, ISO.'),
        query: z.string().optional(),
        limit,
      }),
      execute: args => callTool('festivals', args, opts),
    }),
    experiences: tool({
      description: 'Bookable food tours, cooking classes and tastings in a city, with booking links.',
      inputSchema: z.object({
        city,
        country: country.optional(),
        query: z.string().optional().describe("e.g. 'cooking class', 'wine tasting', 'market tour'."),
        limit,
      }),
      execute: args => callTool('experiences', args, opts),
    }),
    stays: tool({
      description: 'Hotels and places to stay in a city, with booking links.',
      inputSchema: z.object({ country, city, limit: z.number().int().min(1).max(50).optional() }),
      execute: args => callTool('stays', args, opts),
    }),
    dishes: tool({
      description: "A city's signature dishes and where to eat them.",
      inputSchema: z.object({ country: country.optional(), city: city.optional(), query: z.string().optional(), limit }),
      execute: args => callTool('dishes', args, opts),
    }),
    cities: tool({
      description: 'Every city TableJourney covers, with the slugs the other tools accept.',
      inputSchema: z.object({ country: z.string().optional() }),
      execute: args => callTool('cities', args, opts),
    }),
  };
}

export default tablejourneyTools;
