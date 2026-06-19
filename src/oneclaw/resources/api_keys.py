"""API keys resource."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class ApiKeysResource:
    """Personal API key management (``1ck_`` keys)."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        name: str,
        scopes: builtins.list[str] | None = None,
        expires_at: str | None = None,
    ) -> OneclawResponse[Any]:
        """Create a new personal API key. Returns the key value once."""
        body: dict[str, Any] = {"name": name}
        if scopes is not None:
            body["scopes"] = scopes
        if expires_at is not None:
            body["expires_at"] = expires_at
        return self._http.request("POST", "/v1/auth/api-keys", body=body)

    def list(self) -> OneclawResponse[Any]:
        """List all personal API keys."""
        return self._http.request("GET", "/v1/auth/api-keys")

    def delete(self, key_id: str) -> OneclawResponse[Any]:
        """Revoke a personal API key."""
        return self._http.request("DELETE", f"/v1/auth/api-keys/{key_id}")
