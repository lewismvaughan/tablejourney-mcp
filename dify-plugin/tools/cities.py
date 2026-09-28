from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import get_json


class CitiesTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        params = {"country": tool_parameters.get("country")}

        try:
            results = get_json(
                "/cities",
                params=params,
                api_key=self.runtime.credentials.get("api_key"),
            )
        except Exception as exc:
            yield self.create_text_message(f"TableJourney cities lookup failed: {exc}")
            return

        yield self.create_json_message({"results": results, "count": len(results)})
        yield self.create_text_message(_format_cities(results))


def _format_cities(results: list[dict[str, Any]]) -> str:
    if not results:
        return "No cities matched that filter."
    lines = []
    for entry in results:
        name = entry.get("name", "Unknown")
        country_name = entry.get("country_name", "")
        page = entry.get("page", "")
        line = f"{name}, {country_name}" if country_name else name
        if page:
            line = f"{line} ({page})"
        lines.append(line)
    return "\n".join(lines)
