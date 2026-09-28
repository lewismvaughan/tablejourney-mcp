"""Thin HTTP helper shared by every TableJourney tool.

TableJourney's agent API (https://tablejourney.com/api/v1) is public and
read-only: every endpoint below accepts plain GET requests with no
authentication. The optional API key is sent only as an X-API-Key header
for TableJourney's own attribution reporting; it is never required and
unlocks no extra data or rate limit.
"""

from __future__ import annotations

from typing import Any

import requests

BASE_URL = "https://tablejourney.com/api/v1"
TIMEOUT_SECONDS = 15


def get_json(
    path: str,
    params: dict[str, Any] | None = None,
    api_key: str | None = None,
) -> Any:
    """GET a TableJourney API path and return the parsed JSON body.

    ``path`` starts with a slash and is appended to BASE_URL, e.g. "/places".
    ``params`` values that are None or empty strings are dropped so the
    request only carries the filters the caller actually set.
    """
    clean_params = {
        key: value
        for key, value in (params or {}).items()
        if value is not None and value != ""
    }
    headers = {"X-API-Key": api_key} if api_key else {}
    response = requests.get(
        f"{BASE_URL}{path}",
        params=clean_params,
        headers=headers,
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()
