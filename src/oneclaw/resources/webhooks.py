"""Webhooks resource."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class WebhooksResource:
    """Event webhook registration and management."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        url: str,
        events: builtins.list[str],
        *,
        secret: str | None = None,
    ) -> OneclawResponse[Any]:
        """Register a webhook."""
        body: dict[str, Any] = {"url": url, "events": events}
        if secret is not None:
            body["secret"] = secret
        return self._http.request("POST", "/v1/webhooks", body=body)

    def list(self) -> OneclawResponse[Any]:
        """List webhooks for the organization."""
        return self._http.request("GET", "/v1/webhooks")

    def get(self, webhook_id: str) -> OneclawResponse[Any]:
        """Get a webhook by ID."""
        return self._http.request("GET", f"/v1/webhooks/{webhook_id}")

    def update(self, webhook_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Update a webhook (URL, events, active status)."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("PATCH", f"/v1/webhooks/{webhook_id}", body=body)

    def delete(self, webhook_id: str) -> OneclawResponse[Any]:
        """Delete a webhook."""
        return self._http.request("DELETE", f"/v1/webhooks/{webhook_id}")
