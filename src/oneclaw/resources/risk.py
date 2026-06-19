"""Risk engine resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class RiskResource:
    """Risk engine — events, verdicts, and honeytokens."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_events(
        self,
        *,
        severity: str | None = None,
        principal_type: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> OneclawResponse[Any]:
        """List risk events with optional filters."""
        query: dict[str, Any] = {}
        for key, val in {
            "severity": severity, "principal_type": principal_type,
            "limit": limit, "offset": offset,
        }.items():
            if val is not None:
                query[key] = val
        return self._http.request("GET", "/v1/risk/events", query=query or None)

    def list_verdicts(self) -> OneclawResponse[Any]:
        """List active risk verdicts."""
        return self._http.request("GET", "/v1/risk/verdicts")

    def get_verdict(self, principal_type: str, principal_id: str) -> OneclawResponse[Any]:
        """Get the risk verdict for a specific principal."""
        return self._http.request("GET", f"/v1/risk/verdicts/{principal_type}/{principal_id}")

    def create_honeytoken(
        self,
        vault_id: str,
        secret_path: str,
    ) -> OneclawResponse[Any]:
        """Register a canary secret as a honeytoken."""
        return self._http.request(
            "POST", "/v1/risk/honeytokens",
            body={"vault_id": vault_id, "secret_path": secret_path},
        )

    def list_honeytokens(self) -> OneclawResponse[Any]:
        """List registered honeytokens."""
        return self._http.request("GET", "/v1/risk/honeytokens")

    def delete_honeytoken(self, honeytoken_id: str) -> OneclawResponse[Any]:
        """Delete a honeytoken."""
        return self._http.request("DELETE", f"/v1/risk/honeytokens/{honeytoken_id}")
