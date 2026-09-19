"""Pre-built connectors — the catalogue, installs, and polled event sources."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class ConnectorsResource:
    """Connector presets (Gmail, Slack, GitHub, Stripe, …) and event subscriptions."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_presets(self) -> OneclawResponse[Any]:
        """The connector catalogue, including each preset's ``event_sources``. Public."""
        return self._http.request("GET", "/v1/connectors/presets")

    def list(self, agent_id: str) -> OneclawResponse[Any]:
        """Connectors installed on an agent, and whether each is connected."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/connectors")

    def install(
        self,
        agent_id: str,
        slug: str,
        *,
        binding_name: str | None = None,
        scopes: builtins.list[str] | None = None,
        redirect_after: str | None = None,
        host: str | None = None,
        token: str | None = None,
    ) -> OneclawResponse[Any]:
        """Install a connector (human-only). OAuth presets return ``authorization_url``;
        the ``api-token`` preset takes ``host`` and optionally ``token``."""
        body: dict[str, Any] = {}
        if binding_name is not None:
            body["binding_name"] = binding_name
        if scopes is not None:
            body["scopes"] = scopes
        if redirect_after is not None:
            body["redirect_after"] = redirect_after
        if host is not None:
            body["host"] = host
        if token is not None:
            body["token"] = token
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/connectors/{slug}/install", body=body
        )

    # ── Polled event sources → automation events (vault >= 0.61.32) ──

    def subscribe(
        self,
        agent_id: str,
        binding_id: str,
        event_type: str,
        *,
        interval_secs: int | None = None,
    ) -> OneclawResponse[Any]:
        """Subscribe an installed connector binding to one of its preset's event sources
        (e.g. ``gmail.message.received``). 1Claw polls the source through the binding and
        dispatches each new item as an automation event. Human-only; the first poll
        primes the subscription and emits nothing."""
        body: dict[str, Any] = {"binding_id": binding_id, "event_type": event_type}
        if interval_secs is not None:
            body["interval_secs"] = interval_secs
        return self._http.request("POST", f"/v1/agents/{agent_id}/event-subscriptions", body=body)

    def list_subscriptions(self, agent_id: str) -> OneclawResponse[Any]:
        """An agent's event subscriptions."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/event-subscriptions")

    def unsubscribe(self, agent_id: str, subscription_id: str) -> OneclawResponse[Any]:
        """Delete an event subscription (human-only)."""
        return self._http.request(
            "DELETE", f"/v1/agents/{agent_id}/event-subscriptions/{subscription_id}"
        )

    def poll_now(self, agent_id: str, subscription_id: str) -> OneclawResponse[Any]:
        """Poll a subscription now instead of waiting for its interval (human-only)."""
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/event-subscriptions/{subscription_id}/poll"
        )
