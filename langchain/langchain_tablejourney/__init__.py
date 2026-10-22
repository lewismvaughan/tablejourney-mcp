"""TableJourney food travel tools for LangChain.

The tools call TableJourney's public MCP server (https://tablejourney.com/mcp, streamable HTTP, no key needed to
read): verified places to eat with their sources and opening hours, food festivals with the dates of their next
edition, and bookable food tours, cooking classes and stays in 224 cities. An optional partner key
(TABLEJOURNEY_API_KEY) tags every booking link with your partner code: https://tablejourney.com/agents/earn/
"""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Any

from langchain_core.tools import BaseToolkit, StructuredTool
from pydantic import BaseModel, ConfigDict, Field

__all__ = ["TableJourneyClient", "TableJourneyToolkit"]
__version__ = "0.1.0"

ENDPOINT = "https://tablejourney.com/mcp"
USER_AGENT = f"langchain-tablejourney/{__version__}"


class TableJourneyClient:
    """A minimal client for TableJourney's MCP server: one tools/call per request (the server is stateless)."""

    def __init__(self, api_key: str | None = None, endpoint: str = ENDPOINT, timeout: float = 60.0) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("TABLEJOURNEY_API_KEY")
        self.endpoint = endpoint
        self.timeout = timeout

    def call(self, name: str, arguments: dict[str, Any]) -> Any:
        args = {k: v for k, v in arguments.items() if v is not None}
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": name, "arguments": args}})
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "User-Agent": USER_AGENT,
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        req = urllib.request.Request(self.endpoint, data=body.encode(), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=self.timeout) as res:  # noqa: S310 (fixed https endpoint)
            text = res.read().decode()
        if text.startswith(("event:", "data:")):
            text = [ln[5:] for ln in text.splitlines() if ln.startswith("data:")][-1]
        msg = json.loads(text)
        if msg.get("error"):
            raise RuntimeError(f"TableJourney {name}: {msg['error'].get('message')}")
        result = msg.get("result") or {}
        data = _parse(result)
        if result.get("isError"):
            raise RuntimeError(f"TableJourney {name}: {data}")
        return data


def _parse(result: dict[str, Any]) -> Any:
    structured = result.get("structuredContent")
    if structured:
        return structured.get("result", structured)
    items = []
    for c in result.get("content") or []:
        if c.get("type") != "text":
            continue
        try:
            items.append(json.loads(c["text"]))
        except (ValueError, KeyError):
            items.append(c.get("text"))
    return items[0] if len(items) == 1 else items


class _Args(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CityArgs(_Args):
    country: str = Field(description="Country slug or name, e.g. 'italy'.")
    city: str = Field(description="City slug or name, e.g. 'rome' or 'New York City'.")


class ThingsToDoArgs(CityArgs):
    date_from: str | None = Field(default=None, description="Optional trip start, ISO date.")
    date_to: str | None = Field(default=None, description="Optional trip end, ISO date.")


class SearchPlacesArgs(_Args):
    query: str | None = Field(default=None, description="Free text: a venue name, dish, cuisine, neighbourhood or theme.")
    city: str | None = Field(default=None, description="City slug or name.")
    country: str | None = Field(default=None, description="Country slug or name.")
    kind: str | None = Field(default=None, description="restaurants, cafes, bakeries, markets, street-food...")
    cuisine: str | None = None
    dietary: str | None = Field(default=None, description="vegan, vegetarian, gluten-free, halal, kosher...")
    open_at: str | None = Field(default=None, description="'now', 'sunday 10:00' or an ISO datetime (UTC).")
    near: str | None = Field(default=None, description="'lat,lng' to search around a point.")
    limit: int | None = Field(default=None, ge=1, le=100)


class FestivalsArgs(_Args):
    country: str | None = None
    city: str | None = None
    date_from: str | None = Field(default=None, description="Earliest end date to include, ISO. Defaults to today.")
    date_to: str | None = Field(default=None, description="Latest start date to include, ISO.")
    query: str | None = None
    limit: int | None = Field(default=None, ge=1, le=100)


class ExperiencesArgs(_Args):
    city: str = Field(description="City slug or name.")
    country: str | None = None
    query: str | None = Field(default=None, description="e.g. 'cooking class', 'wine tasting', 'market tour'.")
    limit: int | None = Field(default=None, ge=1, le=100)


class StaysArgs(CityArgs):
    limit: int | None = Field(default=None, ge=1, le=50)


class DishesArgs(_Args):
    country: str | None = None
    city: str | None = None
    query: str | None = None
    limit: int | None = Field(default=None, ge=1, le=100)


class CitiesArgs(_Args):
    country: str | None = None


_TOOLS = (
    ("things_to_do", "tablejourney_things_to_do", ThingsToDoArgs,
     "Start here for 'what can I do in <city>?' or trip planning: food tours, tickets, food festivals, places to "
     "eat, stays and car hire for a city in one answer. Give booking links exactly as returned and say once that "
     "they are affiliate links."),
    ("search_places", "tablejourney_search_places", SearchPlacesArgs,
     "Search verified places to eat and drink (restaurants, cafes, bakeries, markets, street food, bars); each "
     "result carries its source, opening hours and a page to cite."),
    ("festivals", "tablejourney_festivals", FestivalsArgs,
     "Food festivals with the dates of their next edition, by country, city or date range."),
    ("experiences", "tablejourney_experiences", ExperiencesArgs,
     "Bookable food tours, cooking classes and tastings in a city, with booking links."),
    ("stays", "tablejourney_stays", StaysArgs, "Hotels and places to stay in a city, with booking links."),
    ("dishes", "tablejourney_dishes", DishesArgs, "A city's signature dishes and where to eat them."),
    ("cities", "tablejourney_cities", CitiesArgs, "Every city TableJourney covers, with the slugs the other tools accept."),
)  # fmt: skip


class TableJourneyToolkit(BaseToolkit):
    """All TableJourney tools. Pass api_key (or set TABLEJOURNEY_API_KEY) to tag booking links with your partner code."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    client: TableJourneyClient = Field(default_factory=TableJourneyClient)

    @classmethod
    def from_api_key(cls, api_key: str | None = None) -> TableJourneyToolkit:
        return cls(client=TableJourneyClient(api_key=api_key))

    def get_tools(self) -> list[StructuredTool]:
        def make(mcp_name: str):
            def run(**kwargs: Any) -> Any:
                return self.client.call(mcp_name, kwargs)

            return run

        return [
            StructuredTool.from_function(func=make(mcp), name=name, description=desc, args_schema=schema)
            for mcp, name, schema, desc in _TOOLS
        ]
