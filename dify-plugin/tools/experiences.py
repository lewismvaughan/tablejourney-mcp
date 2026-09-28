from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import get_json


class ExperiencesTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        params = {
            "country": tool_parameters.get("country"),
            "city": tool_parameters.get("city"),
            "q": tool_parameters.get("q"),
            "partner": tool_parameters.get("partner"),
            "food_only": tool_parameters.get("food_only"),
            "limit": tool_parameters.get("limit"),
        }

        try:
            results = get_json(
                "/experiences",
                params=params,
                api_key=self.runtime.credentials.get("api_key"),
            )
        except Exception as exc:
            yield self.create_text_message(
                f"TableJourney experience search failed: {exc}"
            )
            return

        yield self.create_json_message({"results": results, "count": len(results)})
        yield self.create_text_message(_format_experiences(results))


def _format_experiences(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No bookable experiences matched that search."
    lines = []
    for item in results:
        title = item.get("title", "Unknown")
        price = item.get("price", "")
        rating = item.get("rating", "")
        book = item.get("book", "")
        bits = [title]
        if price:
            bits.append(str(price))
        if rating:
            bits.append(f"rating {rating}")
        line = " - ".join(bits)
        if book:
            line = f"{line} ({book})"
        lines.append(line)
    return "\n".join(lines)
