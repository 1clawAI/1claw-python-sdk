"""Secrets resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class SecretsResource:
    """Secret CRUD within a vault — store, retrieve, list, rotate, version."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def set(
        self,
        vault_id: str,
        key: str,
        value: str,
        *,
        type: str = "generic",
        metadata: dict[str, Any] | None = None,
        expires_at: str | None = None,
        rotation_policy: dict[str, Any] | None = None,
        max_access_count: int | None = None,
    ) -> OneclawResponse[Any]:
        """Store or update a secret at the given path."""
        body: dict[str, Any] = {"type": type, "value": value}
        if metadata is not None:
            body["metadata"] = metadata
        if expires_at is not None:
            body["expires_at"] = expires_at
        if rotation_policy is not None:
            body["rotation_policy"] = rotation_policy
        if max_access_count is not None:
            body["max_access_count"] = max_access_count
        return self._http.request("PUT", f"/v1/vaults/{vault_id}/secrets/{key}", body=body)

    def get(self, vault_id: str, key: str) -> OneclawResponse[Any]:
        """Retrieve a decrypted secret value."""
        return self._http.request("GET", f"/v1/vaults/{vault_id}/secrets/{key}")

    def delete(self, vault_id: str, key: str) -> OneclawResponse[Any]:
        """Delete a secret from a vault."""
        return self._http.request("DELETE", f"/v1/vaults/{vault_id}/secrets/{key}")

    def list(self, vault_id: str, prefix: str | None = None) -> OneclawResponse[Any]:
        """List secret keys (metadata only)."""
        query = {"prefix": prefix} if prefix else None
        return self._http.request("GET", f"/v1/vaults/{vault_id}/secrets", query=query)

    def rotate(
        self,
        vault_id: str,
        key: str,
        new_value: str,
        **kwargs: Any,
    ) -> OneclawResponse[Any]:
        """Rotate a secret by writing a new value (increments version)."""
        return self.set(vault_id, key, new_value, **kwargs)

    def rotate_generate(
        self,
        vault_id: str,
        key: str,
        *,
        length: int | None = None,
        charset: str | None = None,
        type: str | None = None,
    ) -> OneclawResponse[Any]:
        """Server-side rotation: vault generates a cryptographically random value."""
        body: dict[str, Any] = {}
        if length is not None:
            body["length"] = length
        if charset is not None:
            body["charset"] = charset
        if type is not None:
            body["type"] = type
        return self._http.request("POST", f"/v1/vaults/{vault_id}/secret-rotate/{key}", body=body)

    def list_versions(self, vault_id: str, key: str) -> OneclawResponse[Any]:
        """List all versions of a secret at the given path."""
        return self._http.request("GET", f"/v1/vaults/{vault_id}/secret-versions/{key}")

    def get_version(self, vault_id: str, key: str, version: int) -> OneclawResponse[Any]:
        """Retrieve a specific version of a secret."""
        return self._http.request("GET", f"/v1/vaults/{vault_id}/secret-version/{key}/{version}")

    def disable_version(self, vault_id: str, key: str, version: int) -> OneclawResponse[Any]:
        """Disable a version so it can no longer be read (retained for audit)."""
        return self._http.request(
            "POST", f"/v1/vaults/{vault_id}/secret-version-disable/{key}/{version}",
        )
