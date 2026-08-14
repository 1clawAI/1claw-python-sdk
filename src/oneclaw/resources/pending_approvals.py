"""Pending approvals (consensus policy) resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class PendingApprovalsResource:
    """Consensus-based multi-party approval workflow."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def submit(
        self,
        *,
        policy_id: str,
        action: str,
        action_payload: dict[str, Any],
    ) -> OneclawResponse[Any]:
        """Submit an action for human approval."""
        return self._http.request(
            "POST",
            "/v1/pending-approvals",
            body={
                "policy_id": policy_id,
                "action": action,
                "action_payload": action_payload,
            },
        )

    def list(
        self,
        *,
        status: str | None = None,
        agent_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> OneclawResponse[Any]:
        """List pending approvals for the org."""
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if agent_id is not None:
            params["agent_id"] = agent_id
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self._http.request("GET", "/v1/pending-approvals", query=params or None)

    def get(self, approval_id: str) -> OneclawResponse[Any]:
        """Get pending approval details including signatures."""
        return self._http.request("GET", f"/v1/pending-approvals/{approval_id}")

    def approve(
        self,
        approval_id: str,
        *,
        decision: str,
        payload_hash: str,
        reason: str | None = None,
    ) -> OneclawResponse[Any]:
        """Approve or reject a pending approval."""
        body: dict[str, Any] = {"decision": decision, "payload_hash": payload_hash}
        if reason is not None:
            body["reason"] = reason
        return self._http.request(
            "POST",
            f"/v1/pending-approvals/{approval_id}/approve",
            body=body,
        )

    def execute(self, approval_id: str) -> OneclawResponse[Any]:
        """Execute an approved action (human-only)."""
        return self._http.request("POST", f"/v1/pending-approvals/{approval_id}/execute")

    def cancel(self, approval_id: str) -> OneclawResponse[Any]:
        """Cancel a pending approval."""
        return self._http.request("POST", f"/v1/pending-approvals/{approval_id}/cancel")
