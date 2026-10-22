from __future__ import annotations

from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from tools._client import get_json


class TablejourneyProvider(ToolProvider):
    """TableJourney's agent API needs no credentials.

    The provider offers one optional partner key. Validation confirms the
    public API is reachable and, when a key was supplied, that the API
    accepts it (an unknown key is refused by every endpoint, so it is
    better caught here than on the first tool call).
    """

    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = (credentials.get("api_key") or "").strip() or None
        try:
            health = get_json("/health")
        except Exception as exc:
            raise ToolProviderCredentialValidationError(
                f"Could not reach the TableJourney API: {exc}"
            ) from None
        if not health.get("ok"):
            raise ToolProviderCredentialValidationError(
                "TableJourney API responded but reported it is not healthy."
            )
        if api_key:
            try:
                get_json("/cities", params={"country": "malta"}, api_key=api_key)
            except Exception:
                raise ToolProviderCredentialValidationError(
                    "TableJourney did not accept that partner key. Check it, or "
                    "leave the field blank to use the tools without a key."
                ) from None
