"""Agents resource."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class AgentsResource:
    """Agent identity — register, update, delete, rotate keys, transactions."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        name: str,
        *,
        description: str = "",
        auth_method: str = "api_key",
        intents_api_enabled: bool = False,
        shroud_enabled: bool = False,
        shroud_config: dict[str, Any] | None = None,
        token_ttl_seconds: int | None = None,
        vault_ids: builtins.list[str] | None = None,
        scopes: builtins.list[str] | None = None,
        tx_to_allowlist: builtins.list[str] | None = None,
        tx_max_value_eth: str | None = None,
        tx_daily_limit_eth: str | None = None,
        tx_allowed_chains: builtins.list[str] | None = None,
        federation_enabled: bool | None = None,
        federation_audiences: builtins.list[str] | None = None,
        message_signing_enabled: bool | None = None,
        api_key_expires_at: str | None = None,
    ) -> OneclawResponse[Any]:
        """Register a new agent. Returns the agent and a one-time API key."""
        body: dict[str, Any] = {
            "name": name,
            "description": description,
            "auth_method": auth_method,
            "intents_api_enabled": intents_api_enabled,
            "shroud_enabled": shroud_enabled,
        }
        for key, val in {
            "shroud_config": shroud_config,
            "token_ttl_seconds": token_ttl_seconds,
            "vault_ids": vault_ids,
            "scopes": scopes,
            "tx_to_allowlist": tx_to_allowlist,
            "tx_max_value_eth": tx_max_value_eth,
            "tx_daily_limit_eth": tx_daily_limit_eth,
            "tx_allowed_chains": tx_allowed_chains,
            "federation_enabled": federation_enabled,
            "federation_audiences": federation_audiences,
            "message_signing_enabled": message_signing_enabled,
            "api_key_expires_at": api_key_expires_at,
        }.items():
            if val is not None:
                body[key] = val
        return self._http.request("POST", "/v1/agents", body=body)

    def get(self, agent_id: str) -> OneclawResponse[Any]:
        """Fetch an agent by ID."""
        return self._http.request("GET", f"/v1/agents/{agent_id}")

    def me(self) -> OneclawResponse[Any]:
        """Get the calling agent's own profile."""
        return self._http.request("GET", "/v1/agents/me")

    def list(self) -> OneclawResponse[Any]:
        """List all agents in the organization."""
        return self._http.request("GET", "/v1/agents")

    def update(self, agent_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Update an agent's configuration."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("PATCH", f"/v1/agents/{agent_id}", body=body)

    def delete(self, agent_id: str) -> OneclawResponse[Any]:
        """Delete an agent."""
        return self._http.request("DELETE", f"/v1/agents/{agent_id}")

    def rotate_key(self, agent_id: str) -> OneclawResponse[Any]:
        """Rotate an agent's API key. Returns the new key (one-time)."""
        return self._http.request("POST", f"/v1/agents/{agent_id}/rotate-key")

    def rotate_identity_keys(self, agent_id: str) -> OneclawResponse[Any]:
        """Rotate an agent's SSH and ECDH identity keypairs."""
        return self._http.request("POST", f"/v1/agents/{agent_id}/rotate-identity-keys")

    def enroll(
        self, name: str, human_email: str, description: str = ""
    ) -> OneclawResponse[Any]:
        """Self-enroll an agent (no auth required). Credentials emailed to the human."""
        return self._http.request(
            "POST", "/v1/agents/enroll",
            body={"name": name, "human_email": human_email, "description": description},
            skip_auth=True,
        )

    # -- Intents API -----------------------------------------------------------

    def submit_transaction(
        self,
        agent_id: str,
        *,
        chain: str,
        to: str,
        value: str = "0",
        data: str | None = None,
        nonce: int | None = None,
        gas_limit: int | None = None,
        gas_price: str | None = None,
        max_fee_per_gas: str | None = None,
        max_priority_fee_per_gas: str | None = None,
        signing_key_path: str | None = None,
        simulate_first: bool | None = None,
        gasless: bool | None = None,
        treasury_id: str | None = None,
        mode: str | None = None,
        idempotency_key: str | None = None,
    ) -> OneclawResponse[Any]:
        """Submit a transaction via the Intents API."""
        body: dict[str, Any] = {"chain": chain, "to": to, "value": value}
        for key, val in {
            "data": data, "nonce": nonce, "gas_limit": gas_limit,
            "gas_price": gas_price, "max_fee_per_gas": max_fee_per_gas,
            "max_priority_fee_per_gas": max_priority_fee_per_gas,
            "signing_key_path": signing_key_path, "simulate_first": simulate_first,
            "gasless": gasless, "treasury_id": treasury_id, "mode": mode,
        }.items():
            if val is not None:
                body[key] = val
        headers: dict[str, str] | None = None
        if idempotency_key:
            headers = {"Idempotency-Key": idempotency_key}
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/transactions",
            body=body, headers=headers,
        )

    def sign_transaction(self, agent_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Sign a transaction without broadcasting."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("POST", f"/v1/agents/{agent_id}/transactions/sign", body=body)

    def get_transaction(
        self,
        agent_id: str,
        tx_id: str,
        include_signed_tx: bool = False,
    ) -> OneclawResponse[Any]:
        """Get a transaction by ID."""
        query: dict[str, Any] | None = None
        if include_signed_tx:
            query = {"include_signed_tx": "true"}
        return self._http.request("GET", f"/v1/agents/{agent_id}/transactions/{tx_id}", query=query)

    def list_transactions(self, agent_id: str) -> OneclawResponse[Any]:
        """List all transactions for an agent."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/transactions")

    def simulate_transaction(self, agent_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Simulate a transaction via Tenderly."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("POST", f"/v1/agents/{agent_id}/transactions/simulate", body=body)

    def simulate_bundle(
        self, agent_id: str, transactions: builtins.list[dict[str, Any]]
    ) -> OneclawResponse[Any]:
        """Simulate a bundle of transactions."""
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/transactions/simulate-bundle",
            body={"transactions": transactions},
        )

    def sign_intent(self, agent_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Unified signing endpoint (personal_sign, typed_data, transaction)."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("POST", f"/v1/agents/{agent_id}/sign", body=body)

    # -- Smart accounts --------------------------------------------------------

    def add_smart_account(
        self,
        agent_id: str,
        *,
        chain: str,
        chain_id: int,
        safe_address: str,
        nonce: int | None = None,
        init_data: str | None = None,
    ) -> OneclawResponse[Any]:
        """Add a Safe smart account for an agent on a specific chain."""
        body: dict[str, Any] = {
            "chain": chain,
            "chain_id": chain_id,
            "safe_address": safe_address,
        }
        if nonce is not None:
            body["nonce"] = nonce
        if init_data is not None:
            body["init_data"] = init_data
        return self._http.request("POST", f"/v1/agents/{agent_id}/smart-accounts", body=body)

    # -- Bankr keys ------------------------------------------------------------

    def lease_bankr_key(
        self,
        agent_id: str,
        *,
        ttl_seconds: int | None = None,
        wallet_id: str | None = None,
        permissions: dict[str, Any] | None = None,
    ) -> OneclawResponse[Any]:
        """Lease a short-lived Bankr API key."""
        body: dict[str, Any] = {}
        if ttl_seconds is not None:
            body["ttl_seconds"] = ttl_seconds
        if wallet_id is not None:
            body["wallet_id"] = wallet_id
        if permissions is not None:
            body["permissions"] = permissions
        return self._http.request("POST", f"/v1/agents/{agent_id}/bankr-keys/lease", body=body)

    def list_bankr_keys(self, agent_id: str) -> OneclawResponse[Any]:
        """List active Bankr key leases for an agent."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/bankr-keys")

    def revoke_bankr_key(self, agent_id: str, lease_id: str) -> OneclawResponse[Any]:
        """Revoke a Bankr key lease."""
        return self._http.request("DELETE", f"/v1/agents/{agent_id}/bankr-keys/{lease_id}")
