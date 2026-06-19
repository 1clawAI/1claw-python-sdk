"""Approvals resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class ApprovalsResource:
    """Human-in-the-loop approval workflow for agent actions."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def request(
        self,
        *,
        action: str,
        target_type: str,
        target_id: str,
        summary: str,
        reason: str | None = None,
        risk_tier: int | None = None,
    ) -> OneclawResponse[Any]:
        """Create a pending approval request (agent-only)."""
        body: dict[str, Any] = {
            "action": action,
            "target_type": target_type,
            "target_id": target_id,
            "summary": summary,
        }
        if reason is not None:
            body["reason"] = reason
        if risk_tier is not None:
            body["risk_tier"] = risk_tier
        return self._http.request("POST", "/v1/approvals/request", body=body)

    def list(self, status: str | None = None) -> OneclawResponse[Any]:
        """List approval requests."""
        query = {"status": status} if status else None
        return self._http.request("GET", "/v1/approvals", query=query)

    def get(self, approval_id: str) -> OneclawResponse[Any]:
        """Get an approval request by ID."""
        return self._http.request("GET", f"/v1/approvals/{approval_id}")

    def decide(self, approval_id: str, decision: str) -> OneclawResponse[Any]:
        """Approve or reject an approval request."""
        return self._http.request(
            "POST", f"/v1/approvals/{approval_id}/decide",
            body={"decision": decision},
        )
