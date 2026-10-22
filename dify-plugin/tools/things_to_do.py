from __future__ import annotations

from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

from ._client import MISSING_CITY, city_path, get_json

SECTIONS = (
    ("experiences", "Experiences"),
    ("tickets_and_passes", "Tickets and passes"),
    ("festivals", "Food festivals"),
    ("places_to_eat", "Places to eat"),
    ("stays", "Stays"),
    ("car_hire", "Car hire"),
)


class ThingsToDoTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        path = city_path("things-to-do", tool_parameters)
        if not path:
            yield self.create_text_message(MISSING_CITY)
            return
        params = {"from": tool_parameters.get("from"), "to": tool_parameters.get("to")}
        try:
            answer = get_json(path, params=params, api_key=self.runtime.credentials.get("api_key"))
        except Exception as exc:
            yield self.create_text_message(f"TableJourney things_to_do failed: {exc}")
            return

        yield self.create_json_message(answer)
        yield self.create_text_message(_format(answer))


def _format(answer: dict[str, Any]) -> str:
    lines = []
    window = answer.get("window") or {}
    head = f"{answer.get('city', '')}, {answer.get('country', '')}"
    if window:
        head = f"{head} ({window.get('from', '')} to {window.get('to', '')})"
    lines.append(head)
    if answer.get("page"):
        lines.append(f"City guide: {answer['page']}")
    for key, title in SECTIONS:
        items = answer.get(key) or []
        if not items:
            continue
        lines.append("")
        lines.append(f"{title}:")
        for item in items:
            lines.append(f"- {_item_line(item)}")
    return "\n".join(lines)


def _item_line(item: dict[str, Any]) -> str:
    name = item.get("title") or item.get("name") or item.get("partner") or "Unknown"
    bits = [str(name)]
    when = item.get("starts_on")
    if when:
        ends = item.get("ends_on")
        bits.append(f"{when} to {ends}" if ends and ends != when else str(when))
    for key in ("price", "from_price"):
        if item.get(key):
            bits.append(str(item[key]))
    if item.get("rating"):
        bits.append(f"rating {item['rating']}")
    line = ", ".join(bits)
    link = item.get("book") or item.get("booking") or item.get("page")
    return f"{line} ({link})" if link else line
