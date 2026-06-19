"""Treasury resource."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class TreasuryResource:
    """Safe multisig treasuries — CRUD, signers, access requests, proposals."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        name: str,
        safe_address: str,
        *,
        chain: str | None = None,
        chain_id: int | None = None,
        threshold: int | None = None,
        signers: builtins.list[str] | None = None,
    ) -> OneclawResponse[Any]:
        """Create a new treasury."""
        body: dict[str, Any] = {"name": name, "safe_address": safe_address}
        for key, val in {
            "chain": chain, "chain_id": chain_id,
            "threshold": threshold, "signers": signers,
        }.items():
            if val is not None:
                body[key] = val
        return self._http.request("POST", "/v1/treasury", body=body)

    def list(self) -> OneclawResponse[Any]:
        """List all treasuries in the organization."""
        return self._http.request("GET", "/v1/treasury")

    def get(self, treasury_id: str) -> OneclawResponse[Any]:
        """Get a treasury by ID."""
        return self._http.request("GET", f"/v1/treasury/{treasury_id}")

    def update(self, treasury_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Update a treasury."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("PATCH", f"/v1/treasury/{treasury_id}", body=body)

    def delete(self, treasury_id: str) -> OneclawResponse[Any]:
        """Delete a treasury."""
        return self._http.request("DELETE", f"/v1/treasury/{treasury_id}")

    def add_signer(self, treasury_id: str, signer_address: str) -> OneclawResponse[Any]:
        """Add a signer to a treasury."""
        return self._http.request(
            "POST", f"/v1/treasury/{treasury_id}/signers",
            body={"signer_address": signer_address},
        )

    def remove_signer(self, treasury_id: str, signer_address: str) -> OneclawResponse[Any]:
        """Remove a signer from a treasury."""
        return self._http.request("DELETE", f"/v1/treasury/{treasury_id}/signers/{signer_address}")

    def request_access(
        self, treasury_id: str, reason: str | None = None
    ) -> OneclawResponse[Any]:
        """Request access to a treasury (agent-only)."""
        body: dict[str, Any] = {}
        if reason:
            body["reason"] = reason
        return self._http.request("POST", f"/v1/treasury/{treasury_id}/access-requests", body=body)

    def list_access_requests(self, treasury_id: str) -> OneclawResponse[Any]:
        """List access requests for a treasury."""
        return self._http.request("GET", f"/v1/treasury/{treasury_id}/access-requests")

    def approve_access_request(
        self,
        treasury_id: str,
        request_id: str,
        *,
        auto_add_signer: bool | None = None,
        delegation_mode: str | None = None,
        guardrails: dict[str, Any] | None = None,
    ) -> OneclawResponse[Any]:
        """Approve a treasury access request."""
        body: dict[str, Any] = {}
        if auto_add_signer is not None:
            body["auto_add_signer"] = auto_add_signer
        if delegation_mode is not None:
            body["delegation_mode"] = delegation_mode
        if guardrails is not None:
            body["guardrails"] = guardrails
        return self._http.request(
            "POST", f"/v1/treasury/{treasury_id}/access-requests/{request_id}/approve",
            body=body or None,
        )

    def deny_access_request(self, treasury_id: str, request_id: str) -> OneclawResponse[Any]:
        """Deny a treasury access request."""
        return self._http.request(
            "POST", f"/v1/treasury/{treasury_id}/access-requests/{request_id}/deny",
        )

    # -- Proposals -------------------------------------------------------------

    def propose(self, treasury_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Create a multisig proposal."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("POST", f"/v1/treasury/{treasury_id}/proposals", body=body)

    def list_proposals(
        self, treasury_id: str, status: str | None = None
    ) -> OneclawResponse[Any]:
        """List proposals for a treasury."""
        query = {"status": status} if status else None
        return self._http.request("GET", f"/v1/treasury/{treasury_id}/proposals", query=query)

    def get_proposal(self, treasury_id: str, proposal_id: str) -> OneclawResponse[Any]:
        """Get a proposal with collected signatures."""
        return self._http.request("GET", f"/v1/treasury/{treasury_id}/proposals/{proposal_id}")

    def sign_proposal(
        self, treasury_id: str, proposal_id: str, *, signature: str, decision: str = "approve"
    ) -> OneclawResponse[Any]:
        """Submit an EIP-712 signature for a proposal."""
        return self._http.request(
            "POST", f"/v1/treasury/{treasury_id}/proposals/{proposal_id}/sign",
            body={"signature": signature, "decision": decision},
        )

    def execute_proposal(self, treasury_id: str, proposal_id: str) -> OneclawResponse[Any]:
        """Force-execute a proposal if threshold is met."""
        return self._http.request(
            "POST", f"/v1/treasury/{treasury_id}/proposals/{proposal_id}/execute",
        )

    def cancel_proposal(self, treasury_id: str, proposal_id: str) -> OneclawResponse[Any]:
        """Cancel a pending proposal."""
        return self._http.request("DELETE", f"/v1/treasury/{treasury_id}/proposals/{proposal_id}")
