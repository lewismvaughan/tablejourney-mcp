# langchain-tablejourney

[TableJourney](https://tablejourney.com) food travel tools for [LangChain](https://www.langchain.com): verified places to eat (each with its source and opening hours), food festivals with the dates of their next edition, and bookable food tours, cooking classes and stays in 224 cities. No API key is needed.

```bash
pip install langchain-tablejourney
```

```python
from langchain.agents import create_agent
from langchain_tablejourney import TableJourneyToolkit

tools = TableJourneyToolkit().get_tools()
agent = create_agent("openai:gpt-5-mini", tools)
result = agent.invoke({"messages": [{"role": "user", "content": "Plan a food day in Lisbon on Saturday, with one food tour."}]})
print(result["messages"][-1].content)
```

Each tool can also be called directly:

```python
tools = {t.name: t for t in TableJourneyToolkit().get_tools()}
print(tools["tablejourney_festivals"].invoke({"country": "italy", "limit": 3}))
```

## Tools

| Tool | What it does |
| --- | --- |
| `tablejourney_things_to_do` | Food tours, tickets, festivals, places to eat, stays and car hire for a city in one answer |
| `tablejourney_search_places` | Verified restaurants, cafes, bakeries, markets, street food and bars, by query, cuisine, diet or opening time |
| `tablejourney_festivals` | Food festivals with the dates of their next edition |
| `tablejourney_experiences` | Bookable food tours, cooking classes and tastings |
| `tablejourney_stays` | Hotels and places to stay |
| `tablejourney_dishes` | A city's signature dishes and where to eat them |
| `tablejourney_cities` | Every covered city and its slug |

Booking links are affiliate links: pass them on as returned and tell the user once.

## Earn on bookings (optional)

Join the [partner program](https://tablejourney.com/agents/earn/) and set `TABLEJOURNEY_API_KEY` (or use `TableJourneyToolkit.from_api_key("...")`): every booking link the tools return then carries your partner code.

The tools call TableJourney's public MCP server at `https://tablejourney.com/mcp`. Docs: https://tablejourney.com/agents/#langchain
