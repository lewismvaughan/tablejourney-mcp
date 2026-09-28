from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import get_json


class FestivalsTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        params = {
            "country": tool_parameters.get("country"),
            "city": tool_parameters.get("city"),
            "q": tool_parameters.get("q"),
            "from": tool_parameters.get("from"),
            "to": tool_parameters.get("to"),
            "limit": tool_parameters.get("limit"),
        }

        try:
            results = get_json(
                "/festivals",
                params=params,
                api_key=self.runtime.credentials.get("api_key"),
            )
        except Exception as exc:
            yield self.create_text_message(f"TableJourney festival search failed: {exc}")
            return

        yield self.create_json_message({"results": results, "count": len(results)})
        yield self.create_text_message(_format_festivals(results))


def _format_festivals(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No festivals matched that search."
    lines = []
    for festival in results:
        name = festival.get("name", "Unknown")
        starts = festival.get("starts_on", "")
        ends = festival.get("ends_on", "")
        page = festival.get("page", "")
        when = f"{starts} to {ends}" if starts and ends else starts or ""
        line = f"{name}: {when}" if when else name
        if page:
            line = f"{line} ({page})"
        lines.append(line)
    return "\n".join(lines)
