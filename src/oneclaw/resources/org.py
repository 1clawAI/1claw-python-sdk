"""Organization resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class OrgResource:
    """Organization membership, roles, settings, and Bankr config."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def members(self) -> OneclawResponse[Any]:
        """List all members in the organization."""
        return self._http.request("GET", "/v1/org/members")

    def update_member_role(self, user_id: str, role: str) -> OneclawResponse[Any]:
        """Update a member's role."""
        return self._http.request("PATCH", f"/v1/org/members/{user_id}", body={"role": role})

    def remove_member(self, user_id: str) -> OneclawResponse[Any]:
        """Remove a member from the organization."""
        return self._http.request("DELETE", f"/v1/org/members/{user_id}")

    def invite(self, email: str, role: str = "member") -> OneclawResponse[Any]:
        """Invite a user to the organization."""
        return self._http.request("POST", "/v1/org/invite", body={"email": email, "role": role})

    def settings(self) -> OneclawResponse[Any]:
        """Get organization settings."""
        return self._http.request("GET", "/v1/org/settings")

    def update_setting(self, key: str, value: str) -> OneclawResponse[Any]:
        """Update a single organization setting."""
        return self._http.request("PUT", f"/v1/org/settings/{key}", body={"value": value})

    def agent_keys_vault_id(self) -> OneclawResponse[Any]:
        """Get the ID of the org's ``__agent-keys`` vault."""
        return self._http.request("GET", "/v1/org/agent-keys-vault")

    def get_bankr_config(self) -> OneclawResponse[Any]:
        """Get the org's Bankr partner key configuration."""
        return self._http.request("GET", "/v1/org/bankr-config")

    def set_bankr_config(
        self,
        partner_key: str,
        default_wallet_id: str | None = None,
    ) -> OneclawResponse[Any]:
        """Set the org's Bankr partner key configuration."""
        body: dict[str, Any] = {"partner_key": partner_key}
        if default_wallet_id:
            body["default_wallet_id"] = default_wallet_id
        return self._http.request("PUT", "/v1/org/bankr-config", body=body)

    def delete_bankr_config(self) -> OneclawResponse[Any]:
        """Delete the org's Bankr partner key configuration."""
        return self._http.request("DELETE", "/v1/org/bankr-config")

    def get_policy_backend_settings(self) -> OneclawResponse[Any]:
        """Get Cedar/OPA policy backend settings (owner/admin)."""
        return self._http.request("GET", "/v1/org/settings/policy-backend")

    def update_policy_backend_settings(
        self,
        *,
        backend: str | None = None,
        mode: str | None = None,
        scope: list[str] | None = None,
        breaker_behavior: str | None = None,
    ) -> OneclawResponse[Any]:
        """Update Cedar/OPA policy backend settings (owner/admin)."""
        body: dict[str, Any] = {}
        if backend is not None:
            body["backend"] = backend
        if mode is not None:
            body["mode"] = mode
        if scope is not None:
            body["scope"] = scope
        if breaker_behavior is not None:
            body["breaker_behavior"] = breaker_behavior
        return self._http.request("PATCH", "/v1/org/settings/policy-backend", body=body)

    def get_policy_shadow_report(self) -> OneclawResponse[Any]:
        """Get policy shadow mode divergence report (owner/admin)."""
        return self._http.request("GET", "/v1/org/policy-shadow-report")

    def get_guardrail_shadow_report(
        self,
        *,
        since: str | None = None,
        until: str | None = None,
    ) -> OneclawResponse[Any]:
        """Get Convention 6 guardrail shadow violations (owner/admin)."""
        params: dict[str, str] = {}
        if since:
            params["since"] = since
        if until:
            params["until"] = until
        return self._http.request("GET", "/v1/org/guardrail-shadow-report", query=params or None)

    def list_guardrail_revisions(self) -> OneclawResponse[Any]:
        """List guardrail revision history (owner/admin)."""
        return self._http.request("GET", "/v1/org/guardrail-revisions")

    def get_onboarding_status(self) -> OneclawResponse[Any]:
        """Get onboarding progress (welcome bundle, agent, policy, sample secret)."""
        return self._http.request("GET", "/v1/org/onboarding/status")

    def provision_onboarding(
        self,
        *,
        agent_name: str | None = None,
        client: str | None = None,
    ) -> OneclawResponse[Any]:
        """Provision MCP onboarding bundle (human-only; returns one-time ocv_ key)."""
        body: dict[str, Any] = {}
        if agent_name:
            body["agent_name"] = agent_name
        if client:
            body["client"] = client
        return self._http.request("POST", "/v1/onboarding/provision", body=body)
