async function search_food_places(params) {
  const url = new URL("https://tablejourney.com/api/v1/places");
  for (const key of ["q", "city", "country", "cuisine", "dietary"]) {
    if (params[key]) url.searchParams.set(key, params[key]);
  }
  url.searchParams.set("limit", "10");
  const response = await fetch(url.toString());
  if (!response.ok) {
    return `TableJourney API error: HTTP ${response.status}`;
  }
  return await response.json();
}
