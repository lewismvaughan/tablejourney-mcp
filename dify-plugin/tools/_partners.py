"""Shared text format for partner lists (tickets, car hire)."""

from __future__ import annotations

from typing import Any


def format_partners(results: list[dict[str, Any]], empty: str) -> str:
    if not results:
        return empty
    lines = []
    for item in results:
        bits = [item.get("partner", "Unknown")]
        pickups = item.get("pickups") or []
        if pickups:
            bits.append("pick-up at " + ", ".join(pickups[:3]))
        if item.get("checked_on"):
            bits.append(f"checked {item['checked_on']}")
        line = ", ".join(bits)
        if item.get("book"):
            line = f"{line} ({item['book']})"
        lines.append(f"- {line}")
    return "\n".join(lines)
