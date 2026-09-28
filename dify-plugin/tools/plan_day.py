from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import get_json


class PlanDayTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        country = (tool_parameters.get("country") or "").strip()
        city = (tool_parameters.get("city") or "").strip()
        if not country or not city:
            yield self.create_text_message(
                "Both country and city are required, as TableJourney's own URL slugs, "
                "for example country=japan and city=tokyo."
            )
            return

        params = {
            "neighborhood": tool_parameters.get("neighborhood"),
            "dietary": tool_parameters.get("dietary"),
            "price_tier": tool_parameters.get("price_tier"),
            "date": tool_parameters.get("date"),
        }

        try:
            plan = get_json(
                f"/plan/{country}/{city}",
                params=params,
                api_key=self.runtime.credentials.get("api_key"),
            )
        except Exception as exc:
            yield self.create_text_message(f"TableJourney plan_day failed: {exc}")
            return

        yield self.create_json_message(plan)
        yield self.create_text_message(_format_plan(plan))


def _format_plan(plan: dict[str, Any]) -> str:
    slots = plan.get("plan") or []
    if not slots:
        return "No plan could be composed for that city and filters."
    lines = []
    for entry in slots:
        slot = entry.get("slot", "")
        around = entry.get("around", "")
        place = entry.get("place") or {}
        name = place.get("name", "Unknown")
        page = place.get("page", "")
        header = f"{slot} ({around})" if around else slot
        line = f"{header}: {name}"
        if page:
            line = f"{line} ({page})"
        lines.append(line)
    return "\n".join(lines)
