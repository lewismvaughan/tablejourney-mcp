"""TableJourney tools for Haystack (tested with haystack-ai 3.2).

No package to install beyond haystack-ai and requests. Copy this file into
your project and import `tablejourney_tools`.
"""

import requests
from haystack.tools import Tool

TABLEJOURNEY_API = "https://tablejourney.com/api/v1"


def search_food_places(
    q: str = "",
    city: str = "",
    country: str = "",
    cuisine: str = "",
    dietary: str = "",
    limit: int = 10,
) -> dict | list:
    """Search verified restaurants, cafes, markets and street food across
    214 cities. Every result carries a provenance URL and last-checked date."""
    params = {
        "q": q,
        "city": city,
        "country": country,
        "cuisine": cuisine,
        "dietary": dietary,
        "limit": limit,
    }
    params = {k: v for k, v in params.items() if v}
    response = requests.get(f"{TABLEJOURNEY_API}/places", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def plan_food_day(country: str, city: str, dietary: str = "", price_tier: str = "") -> dict | list:
    """Compose a one-day food itinerary for a city from verified, open venues."""
    params = {k: v for k, v in {"dietary": dietary, "price_tier": price_tier}.items() if v}
    response = requests.get(
        f"{TABLEJOURNEY_API}/plan/{country}/{city}", params=params, timeout=10
    )
    response.raise_for_status()
    return response.json()


def find_food_festivals(city: str = "", country: str = "", q: str = "") -> dict | list:
    """Find food festivals with resolved next-occurrence dates."""
    params = {k: v for k, v in {"city": city, "country": country, "q": q}.items() if v}
    response = requests.get(f"{TABLEJOURNEY_API}/festivals", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


tablejourney_search_tool = Tool(
    name="search_food_places",
    description=(
        "Search verified restaurants, cafes, markets and street food across "
        "214 cities. Returns venue name, address, cuisine, price tier, hours "
        "and a source URL for each result."
    ),
    function=search_food_places,
    parameters={
        "type": "object",
        "properties": {
            "q": {"type": "string", "description": "Free text: a dish, cuisine or neighborhood"},
            "city": {"type": "string"},
            "country": {"type": "string"},
            "cuisine": {"type": "string"},
            "dietary": {"type": "string", "description": "e.g. vegan, vegetarian, halal, gluten-free"},
            "limit": {"type": "integer", "default": 10},
        },
    },
)

tablejourney_plan_tool = Tool(
    name="plan_food_day",
    description="Compose a one-day food itinerary for a city from verified, open venues.",
    function=plan_food_day,
    parameters={
        "type": "object",
        "properties": {
            "country": {"type": "string"},
            "city": {"type": "string"},
            "dietary": {"type": "string"},
            "price_tier": {"type": "string"},
        },
        "required": ["country", "city"],
    },
)

tablejourney_festivals_tool = Tool(
    name="find_food_festivals",
    description="Find food festivals with resolved next-occurrence dates.",
    function=find_food_festivals,
    parameters={
        "type": "object",
        "properties": {
            "city": {"type": "string"},
            "country": {"type": "string"},
            "q": {"type": "string"},
        },
    },
)
