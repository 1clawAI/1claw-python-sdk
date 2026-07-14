"""Payment Card Vault resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from uuid import uuid4

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class CardsResource:
    """Payment Card Vault — order prepaid/gift cards via x402, then list, get,
    refresh, void, and (human-gated) reveal them.

    PANs/CVVs are never returned except by :meth:`reveal`, which requires human
    password re-authentication (or an explicit per-card agent reveal policy).
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def order(
        self,
        agent_id: str,
        kind: str,
        amount_usd: str,
        *,
        laso_server_id: str | None = None,
        country: str | None = None,
        idempotency_key: str | None = None,
    ) -> OneclawResponse[Any]:
        """Order a prepaid or gift card for an agent.

        Drives the x402 payment flow server-side using the agent's Ethereum
        signing key (funded with USDC on Base).  An ``Idempotency-Key`` header
        is generated automatically; pass *idempotency_key* to override.
        """
        body: dict[str, Any] = {"kind": kind, "amount_usd": amount_usd}
        if laso_server_id is not None:
            body["laso_server_id"] = laso_server_id
        if country is not None:
            body["country"] = country

        key = idempotency_key or str(uuid4())
        return self._http.request(
            "POST",
            f"/v1/agents/{agent_id}/cards/order",
            body=body,
            headers={"Idempotency-Key": key},
        )

    def list(self) -> OneclawResponse[Any]:
        """List cards for the caller (agents see only their own). Always masked."""
        return self._http.request("GET", "/v1/cards")

    def get(self, card_id: str) -> OneclawResponse[Any]:
        """Get a single card (masked — last4 only)."""
        return self._http.request("GET", f"/v1/cards/{card_id}")

    def reveal(
        self,
        card_id: str,
        *,
        password: str | None = None,
    ) -> OneclawResponse[Any]:
        """Reveal full card details.

        Humans must pass their account password via *password* (sent as
        ``X-Auth-Confirm``).  Agents may reveal only when a human has enabled
        a per-card reveal policy.
        """
        headers: dict[str, str] | None = None
        if password is not None:
            headers = {"X-Auth-Confirm": password}
        return self._http.request(
            "POST",
            f"/v1/cards/{card_id}/reveal",
            headers=headers,
        )

    def update(
        self,
        card_id: str,
        *,
        reveal_policy: dict[str, Any] | None = None,
        void_after: str | None = None,
    ) -> OneclawResponse[Any]:
        """Update a card's reveal policy and/or void_after (human-only)."""
        body: dict[str, Any] = {}
        if reveal_policy is not None:
            body["reveal_policy"] = reveal_policy
        if void_after is not None:
            body["void_after"] = void_after
        return self._http.request("PATCH", f"/v1/cards/{card_id}", body=body)

    def void(self, card_id: str) -> OneclawResponse[Any]:
        """Void a card — a 1Claw-level lock. Forward-looking only."""
        return self._http.request("POST", f"/v1/cards/{card_id}/void")

    def refresh(self, card_id: str) -> OneclawResponse[Any]:
        """Refresh a Laso reference-mode card's balance/status. Rate-limited."""
        return self._http.request("POST", f"/v1/cards/{card_id}/refresh")

    def import_card(
        self,
        *,
        pan: str,
        cvv: str,
        exp_month: int,
        exp_year: int,
        brand: str | None = None,
        currency: str | None = None,
        balance: str | None = None,
        agent_id: str | None = None,
    ) -> OneclawResponse[Any]:
        """Manually import an existing card (human-only, full storage mode)."""
        body: dict[str, Any] = {
            "pan": pan,
            "cvv": cvv,
            "exp_month": exp_month,
            "exp_year": exp_year,
        }
        for key, val in {
            "brand": brand,
            "currency": currency,
            "balance": balance,
            "agent_id": agent_id,
        }.items():
            if val is not None:
                body[key] = val
        return self._http.request("POST", "/v1/cards/import", body=body)

    def search_gift_cards(
        self,
        *,
        query: str | None = None,
        country: str | None = None,
    ) -> OneclawResponse[Any]:
        """Search available Laso gift-card brands/servers."""
        body: dict[str, Any] = {}
        if query is not None:
            body["query"] = query
        if country is not None:
            body["country"] = country
        return self._http.request("POST", "/v1/cards/gift-cards/search", body=body)
