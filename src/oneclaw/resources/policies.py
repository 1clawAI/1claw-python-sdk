"""Access policies resource."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class PoliciesResource:
    """Access policy management for vaults."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        vault_id: str,
        *,
        principal_type: str,
        principal_id: str,
        secret_path_pattern: str,
        permissions: builtins.list[str] | None = None,
        conditions: dict[str, Any] | None = None,
        expires_at: str | None = None,
    ) -> OneclawResponse[Any]:
        """Create an access policy on a vault."""
        body: dict[str, Any] = {
            "principal_type": principal_type,
            "principal_id": principal_id,
            "secret_path_pattern": secret_path_pattern,
            "permissions": permissions or ["read"],
        }
        if conditions is not None:
            body["conditions"] = conditions
        if expires_at is not None:
            body["expires_at"] = expires_at
        return self._http.request("POST", f"/v1/vaults/{vault_id}/policies", body=body)

    def list(self, vault_id: str) -> OneclawResponse[Any]:
        """List all policies on a vault."""
        return self._http.request("GET", f"/v1/vaults/{vault_id}/policies")

    def update(
        self,
        vault_id: str,
        policy_id: str,
        *,
        permissions: builtins.list[str] | None = None,
        conditions: dict[str, Any] | None = None,
        expires_at: str | None = None,
    ) -> OneclawResponse[Any]:
        """Update a policy's permissions, conditions, or expiry."""
        body: dict[str, Any] = {}
        if permissions is not None:
            body["permissions"] = permissions
        if conditions is not None:
            body["conditions"] = conditions
        if expires_at is not None:
            body["expires_at"] = expires_at
        return self._http.request("PUT", f"/v1/vaults/{vault_id}/policies/{policy_id}", body=body)

    def delete(self, vault_id: str, policy_id: str) -> OneclawResponse[Any]:
        """Delete a policy."""
        return self._http.request("DELETE", f"/v1/vaults/{vault_id}/policies/{policy_id}")
