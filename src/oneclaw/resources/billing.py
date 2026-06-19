"""Billing resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class BillingResource:
    """Billing — subscriptions, credits, usage, and LLM token billing."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def subscription(self) -> OneclawResponse[Any]:
        """Get the current subscription, usage, and credit summary."""
        return self._http.request("GET", "/v1/billing/subscription")

    def subscribe(
        self, price_id: str | None = None, interval: str | None = None
    ) -> OneclawResponse[Any]:
        """Create a Stripe Checkout session for a subscription."""
        body: dict[str, Any] = {}
        if price_id:
            body["price_id"] = price_id
        if interval:
            body["interval"] = interval
        return self._http.request("POST", "/v1/billing/subscribe", body=body)

    def portal(self) -> OneclawResponse[Any]:
        """Get a Stripe Customer Portal URL."""
        return self._http.request("POST", "/v1/billing/portal")

    def credit_balance(self) -> OneclawResponse[Any]:
        """Get the current credit balance and expiring credits."""
        return self._http.request("GET", "/v1/billing/credits/balance")

    def credit_transactions(self) -> OneclawResponse[Any]:
        """Get the credit transaction ledger."""
        return self._http.request("GET", "/v1/billing/credits/transactions")

    def credit_topup(self, amount_cents: int) -> OneclawResponse[Any]:
        """Create a Stripe Checkout session for a credit top-up."""
        return self._http.request(
            "POST", "/v1/billing/credits/topup",
            body={"amount_cents": amount_cents},
        )

    def set_overage_method(self, method: str) -> OneclawResponse[Any]:
        """Toggle between ``credits`` and ``x402`` overage methods."""
        return self._http.request("PATCH", "/v1/billing/overage-method", body={"method": method})

    def llm_token_billing(self) -> OneclawResponse[Any]:
        """Get LLM token billing status."""
        return self._http.request("GET", "/v1/billing/llm-token-billing")

    def subscribe_llm_token_billing(self) -> OneclawResponse[Any]:
        """Subscribe to LLM token billing via Stripe."""
        return self._http.request("POST", "/v1/billing/llm-token-billing/subscribe")

    def disable_llm_token_billing(self) -> OneclawResponse[Any]:
        """Disable LLM token billing."""
        return self._http.request("POST", "/v1/billing/llm-token-billing/disable")
