from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import MISSING_CITY, city_path, get_json


class ItinerariesTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        path = city_path("itineraries", tool_parameters)
        if not path:
            yield self.create_text_message(MISSING_CITY)
            return
        try:
            results = get_json(path, api_key=self.runtime.credentials.get("api_key"))
        except Exception as exc:
            yield self.create_text_message(f"TableJourney itineraries lookup failed: {exc}")
            return

        yield self.create_json_message({"results": results, "count": len(results)})
        yield self.create_text_message(_format(results))


def _format(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No itineraries are written for that city yet; plan_day can compose a day."
    lines = []
    for itinerary in results:
        lines.append(itinerary.get("title", "Itinerary"))
        for day in itinerary.get("days") or []:
            names = [v.get("name", "") for v in day.get("venues") or [] if v.get("name")]
            line = f"- {day.get('title', '')}"
            if names:
                line = f"{line}: " + ", ".join(names)
            lines.append(line)
        lines.append("")
    return "\n".join(lines).strip()
