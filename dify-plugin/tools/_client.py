"""Thin HTTP helper shared by every TableJourney tool.

TableJourney's agent API (https://tablejourney.com/api/v1) is public and
read-only: every endpoint below accepts plain GET requests with no
authentication. The optional partner key is sent as an X-API-Key header;
its only effect is that the booking links in each answer carry the key
holder's partner code.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any
from urllib.parse import quote

import requests

BASE_URL = "https://tablejourney.com/api/v1"
TIMEOUT_SECONDS = 20
USER_AGENT = "tablejourney-dify-plugin/0.0.2"


class TableJourneyError(Exception):
    """A readable API error, never carrying the key."""


def slug(value: Any) -> str:
    """A path segment from a city or country the caller gave (slug or name)."""
    text = str(value or "").strip()
    return quote(text, safe="")


def to_slug(value: Any) -> str:
    """Slug for filters that only take one: "United States" becomes "united-states"."""
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def get_json(
    path: str,
    params: dict[str, Any] | None = None,
    api_key: str | None = None,
) -> Any:
    """GET a TableJourney API path and return the parsed JSON body.

    ``path`` starts with a slash and is appended to BASE_URL, e.g. "/places".
    ``params`` values that are None or empty strings are dropped so the
    request only carries the filters the caller actually set. An error
    answer from the API (unknown city and the like) is raised as
    TableJourneyError with the API's own message and suggestions.
    """
    clean_params = {
        key: _param(value)
        for key, value in (params or {}).items()
        if value is not None and value != ""
    }
    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if api_key:
        headers["X-API-Key"] = api_key.strip()
    response = requests.get(
        f"{BASE_URL}{path}",
        params=clean_params,
        headers=headers,
        timeout=TIMEOUT_SECONDS,
    )
    if response.status_code >= 400:
        raise TableJourneyError(_error_text(response))
    return response.json()


def _param(value: Any) -> Any:
    """Dify passes numbers as floats and booleans as bools; send 20, not 20.0, and true."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str):
        return value.strip()
    return value


def _error_text(response: requests.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return f"HTTP {response.status_code}"
    if not isinstance(body, dict):
        return f"HTTP {response.status_code}"
    message = body.get("error") or body.get("detail") or f"HTTP {response.status_code}"
    if not isinstance(message, str):
        message = f"HTTP {response.status_code}"
    suggestions = body.get("did_you_mean") or []
    if suggestions:
        names = ", ".join(_suggestion(s) for s in suggestions[:5])
        message = f"{message}. Did you mean: {names}?"
    hint = body.get("hint")
    if isinstance(hint, str) and hint:
        message = f"{message} ({hint})"
    return message


def _suggestion(item: Any) -> str:
    if isinstance(item, dict):
        city = item.get("city") or item.get("name") or ""
        country = item.get("country") or ""
        return f"{city} ({country})" if country else str(city)
    return str(item)


def city_path(prefix: str, tool_parameters: dict[str, Any]) -> str | None:
    """``/<prefix>/<country>/<city>`` or None when either is missing."""
    country = slug(tool_parameters.get("country"))
    city = slug(tool_parameters.get("city"))
    if not country or not city:
        return None
    return f"/{prefix}/{country}/{city}"


MISSING_CITY = (
    "Both country and city are required, as slugs or names, for example "
    "country=italy and city=rome. The cities tool lists every covered city."
)
