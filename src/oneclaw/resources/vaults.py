"""Vault resource."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class VaultResource:
    """Vault lifecycle — create, list, get, delete, CMEK, MPC."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        name: str,
        description: str = "",
        mpc_custody: str | None = None,
    ) -> OneclawResponse[Any]:
        """Create a new encrypted vault."""
        body: dict[str, Any] = {"name": name, "description": description}
        if mpc_custody:
            body["mpc_custody"] = mpc_custody
        return self._http.request("POST", "/v1/vaults", body=body)

    def get(self, vault_id: str) -> OneclawResponse[Any]:
        """Fetch a single vault by ID."""
        return self._http.request("GET", f"/v1/vaults/{vault_id}")

    def list(self) -> OneclawResponse[Any]:
        """List all vaults visible to the authenticated identity."""
        return self._http.request("GET", "/v1/vaults")

    def delete(self, vault_id: str) -> OneclawResponse[Any]:
        """Permanently delete a vault and all its secrets."""
        return self._http.request("DELETE", f"/v1/vaults/{vault_id}")

    def enable_cmek(self, vault_id: str, fingerprint: str) -> OneclawResponse[Any]:
        """Enable Customer-Managed Encryption Key on a vault."""
        return self._http.request(
            "POST", f"/v1/vaults/{vault_id}/cmek",
            body={"fingerprint": fingerprint},
        )

    def disable_cmek(self, vault_id: str) -> OneclawResponse[Any]:
        """Disable CMEK on a vault."""
        return self._http.request("DELETE", f"/v1/vaults/{vault_id}/cmek")

    def enable_mpc(
        self,
        vault_id: str,
        custody_mode: str,
        providers: builtins.list[str] | None = None,
    ) -> OneclawResponse[Any]:
        """Enable Multi-Party Computation on a vault."""
        body: dict[str, Any] = {"custody_mode": custody_mode}
        if providers:
            body["providers"] = providers
        return self._http.request("POST", f"/v1/vaults/{vault_id}/mpc", body=body)

    def rotate_cmek(
        self,
        vault_id: str,
        old_key_base64: str,
        new_key_base64: str,
        new_fingerprint: str,
    ) -> OneclawResponse[Any]:
        """Start a server-assisted CMEK key rotation job."""
        return self._http.request(
            "POST", f"/v1/vaults/{vault_id}/cmek-rotate",
            body={"new_fingerprint": new_fingerprint},
            headers={
                "x-cmek-old-key": old_key_base64,
                "x-cmek-new-key": new_key_base64,
            },
        )

    def get_rotation_job_status(self, vault_id: str, job_id: str) -> OneclawResponse[Any]:
        """Poll the status of a CMEK rotation job."""
        return self._http.request("GET", f"/v1/vaults/{vault_id}/cmek-rotate/{job_id}")
