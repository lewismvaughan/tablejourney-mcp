from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import get_json


class SearchPlacesTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        params = {
            "q": tool_parameters.get("q"),
            "country": tool_parameters.get("country"),
            "city": tool_parameters.get("city"),
            "kind": tool_parameters.get("kind"),
            "cuisine": tool_parameters.get("cuisine"),
            "dietary": tool_parameters.get("dietary"),
            "price_tier": tool_parameters.get("price_tier"),
            "near": tool_parameters.get("near"),
            "radius_km": tool_parameters.get("radius_km"),
            "open_only": tool_parameters.get("open_only"),
            "open_at": tool_parameters.get("open_at"),
            "limit": tool_parameters.get("limit"),
            "offset": tool_parameters.get("offset"),
        }

        try:
            results = get_json(
                "/places",
                params=params,
                api_key=self.runtime.credentials.get("api_key"),
            )
        except Exception as exc:
            yield self.create_text_message(
                f"TableJourney place search failed: {exc}"
            )
            return

        yield self.create_json_message({"results": results, "count": len(results)})
        yield self.create_text_message(_format_places(results))


def _format_places(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No verified places matched that search."
    lines = []
    for place in results:
        name = place.get("name", "Unknown")
        cuisine = place.get("cuisine", "")
        neighborhood = place.get("neighborhood", "")
        price = place.get("price_tier", "")
        page = place.get("page", "")
        bits = [name]
        if cuisine:
            bits.append(cuisine)
        if neighborhood:
            bits.append(neighborhood)
        if price:
            bits.append(price)
        line = " - ".join(bits)
        if page:
            line = f"{line} ({page})"
        lines.append(line)
    return "\n".join(lines)
