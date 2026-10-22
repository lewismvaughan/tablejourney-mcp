# tablejourney-ai-sdk

[TableJourney](https://tablejourney.com) food travel tools for the [Vercel AI SDK](https://ai-sdk.dev): verified places to eat (each with its source and opening hours), food festivals with the dates of their next edition, and bookable food tours, cooking classes and stays in 224 cities. No API key is needed.

```bash
npm install tablejourney-ai-sdk ai zod
```

```ts
import { generateText, isStepCount } from 'ai';
import { tablejourneyTools } from 'tablejourney-ai-sdk';

const { text } = await generateText({
  model: 'openai/gpt-5-mini',
  tools: tablejourneyTools(),
  stopWhen: isStepCount(5),
  prompt: 'Plan a food day in Lisbon on Saturday, with one food tour.',
});

console.log(text);
```

## Tools

| Tool | What it does |
| --- | --- |
| `thingsToDo` | Food tours, tickets, festivals, places to eat, stays and car hire for a city in one answer |
| `searchPlaces` | Verified restaurants, cafes, bakeries, markets, street food and bars, by query, cuisine, diet or opening time |
| `festivals` | Food festivals with the dates of their next edition |
| `experiences` | Bookable food tours, cooking classes and tastings |
| `stays` | Hotels and places to stay |
| `dishes` | A city's signature dishes and where to eat them |
| `cities` | Every covered city and its slug |

Booking links are affiliate links: pass them on as returned and tell the user once.

## Earn on bookings (optional)

Join the [partner program](https://tablejourney.com/agents/earn/) and set `TABLEJOURNEY_API_KEY` (or pass `tablejourneyTools({ apiKey })`): every booking link the tools return then carries your partner code, and you keep a share of the commission TableJourney is paid on those bookings.

The tools call TableJourney's public MCP server at `https://tablejourney.com/mcp`. Docs: https://tablejourney.com/agents/#ai-sdk
