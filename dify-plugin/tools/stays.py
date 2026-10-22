from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import MISSING_CITY, city_path, get_json


class StaysTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        path = city_path("stays", tool_parameters)
        if not path:
            yield self.create_text_message(MISSING_CITY)
            return
        limit = tool_parameters.get("limit")
        params = {"limit": int(limit) if limit else None}
        try:
            answer = get_json(path, params=params, api_key=self.runtime.credentials.get("api_key"))
        except Exception as exc:
            yield self.create_text_message(f"TableJourney stays lookup failed: {exc}")
            return

        yield self.create_json_message(answer)
        yield self.create_text_message(_format(answer))


def _format(answer: dict[str, Any]) -> str:
    hotels = answer.get("hotels") or []
    partners = answer.get("partners") or []
    if not hotels and not partners:
        return "No stays are listed for that city."
    lines = []
    for hotel in hotels:
        bits = [hotel.get("name", "Unknown")]
        if hotel.get("partner"):
            bits.append(f"on {hotel['partner']}")
        near = hotel.get("near") or []
        if near:
            bits.append("near " + ", ".join(near[:2]))
        line = ", ".join(bits)
        if hotel.get("book"):
            line = f"{line} ({hotel['book']})"
        lines.append(f"- {line}")
    for partner in partners:
        bits = [partner.get("partner", "Unknown")]
        if partner.get("from_price"):
            bits.append(f"from {partner['from_price']}")
        line = ", ".join(bits)
        if partner.get("book"):
            line = f"{line} ({partner['book']})"
        lines.append(f"- {line}")
    return "\n".join(lines)
