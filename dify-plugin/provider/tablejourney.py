from __future__ import annotations

from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools._client import get_json


class TablejourneyProvider(ToolProvider):
    """TableJourney's agent API needs no credentials at all.

    The provider only offers an optional attribution key, so validation
    just confirms the public API is reachable, regardless of whether a key
    was supplied.
    """

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            health = get_json("/health", api_key=credentials.get("api_key"))
        except Exception as exc:
            raise ToolProviderCredentialValidationError(
                f"Could not reach the TableJourney API: {exc}"
            ) from None
        if not health.get("ok"):
            raise ToolProviderCredentialValidationError(
                "TableJourney API responded but reported it is not healthy."
            )
