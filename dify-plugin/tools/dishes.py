from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import get_json


class DishesTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        limit = tool_parameters.get("limit")
        params = {
            "country": tool_parameters.get("country"),
            "city": tool_parameters.get("city"),
            "q": tool_parameters.get("q"),
            "limit": int(limit) if limit else None,
        }
        try:
            results = get_json(
                "/dishes", params=params, api_key=self.runtime.credentials.get("api_key")
            )
        except Exception as exc:
            yield self.create_text_message(f"TableJourney dishes lookup failed: {exc}")
            return

        yield self.create_json_message({"results": results, "count": len(results)})
        yield self.create_text_message(_format(results))


def _format(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No signature dishes matched that search."
    lines = []
    for dish in results:
        line = dish.get("name", "Unknown")
        if dish.get("page"):
            line = f"{line} ({dish['page']})"
        venues = [v.get("name", "") for v in dish.get("where_to_eat") or [] if v.get("name")]
        if venues:
            line = f"{line}: eat it at " + ", ".join(venues[:4])
        lines.append(f"- {line}")
    return "\n".join(lines)
