from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import get_json, slug


class PlaceTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        parts = [p for p in str(tool_parameters.get("id") or "").strip().split("/") if p]
        if len(parts) != 4:
            yield self.create_text_message(
                "The place id has four parts, country/city/kind/slug, exactly as "
                "search_places returned it, for example italy/rome/bakeries/insieme-al-pane."
            )
            return
        path = "/places/" + "/".join(slug(p) for p in parts)
        try:
            place = get_json(path, api_key=self.runtime.credentials.get("api_key"))
        except Exception as exc:
            yield self.create_text_message(f"TableJourney place lookup failed: {exc}")
            return

        yield self.create_json_message(place)
        yield self.create_text_message(_format(place))


def _format(place: dict[str, Any]) -> str:
    lines = [place.get("name", "Unknown")]
    if place.get("summary"):
        lines.append(place["summary"])
    if "open_now_utc" in place:
        state = {True: "open now", False: "closed now"}.get(place["open_now_utc"], "hours unknown")
        lines.append(f"Status: {state}")
    if place.get("page"):
        lines.append(f"Page: {place['page']}")
    nearby = place.get("nearby") or []
    if nearby:
        lines.append("Nearby:")
        for item in nearby:
            dist = item.get("distance_km")
            extra = f", {dist} km" if dist is not None else ""
            lines.append(f"- {item.get('name', '')}{extra} ({item.get('page', '')})")
    return "\n".join(lines)
