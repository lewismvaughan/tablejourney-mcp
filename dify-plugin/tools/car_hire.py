from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import MISSING_CITY, city_path, get_json
from ._partners import format_partners


class CarHireTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        path = city_path("cars", tool_parameters)
        if not path:
            yield self.create_text_message(MISSING_CITY)
            return
        try:
            results = get_json(path, api_key=self.runtime.credentials.get("api_key"))
        except Exception as exc:
            yield self.create_text_message(f"TableJourney car hire lookup failed: {exc}")
            return

        yield self.create_json_message({"results": results, "count": len(results)})
        yield self.create_text_message(
            format_partners(results, "No car hire partners are listed for that city.")
        )
