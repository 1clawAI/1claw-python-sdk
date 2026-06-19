"""Signing keys resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class SigningKeysResource:
    """Per-agent multi-chain signing key management."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(self, agent_id: str, chain: str) -> OneclawResponse[Any]:
        """Provision a signing key for an agent on a specific chain."""
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/signing-keys",
            body={"chain": chain},
        )

    def list(self, agent_id: str) -> OneclawResponse[Any]:
        """List all signing keys for an agent."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/signing-keys")

    def rotate(self, agent_id: str, chain: str) -> OneclawResponse[Any]:
        """Rotate a signing key for a specific chain."""
        return self._http.request("POST", f"/v1/agents/{agent_id}/signing-keys/{chain}/rotate")

    def deactivate(self, agent_id: str, chain: str) -> OneclawResponse[Any]:
        """Deactivate a signing key for a specific chain."""
        return self._http.request("DELETE", f"/v1/agents/{agent_id}/signing-keys/{chain}")

    def export(self, agent_id: str, chain: str, password: str) -> OneclawResponse[Any]:
        """Export a signing key (requires password re-authentication)."""
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/signing-keys/{chain}/export",
            headers={"X-Auth-Confirm": password},
        )

    def balance(self, agent_id: str, chain: str) -> OneclawResponse[Any]:
        """Get the balance for a signing key's address."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/signing-keys/{chain}/balance")
