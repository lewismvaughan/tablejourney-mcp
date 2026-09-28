# TableJourney tools for Haystack

`tablejourney_tools.py` defines three Haystack `Tool`s over TableJourney's public,
free, no-auth food travel API (https://tablejourney.com/api/v1):

- `search_food_places`: verified restaurants, cafes, markets and street food in 214 cities, each with its source URL and last-checked date
- `plan_food_day`: a one-day food itinerary for a city from verified, open venues
- `find_food_festivals`: food festivals with resolved next dates

Install `haystack-ai` and `requests`, copy the file into your project, and pass the
tools to a Haystack `Agent`. Tested with haystack-ai 3.2. MIT licensed.
Agent terms: https://tablejourney.com/agents/#terms
