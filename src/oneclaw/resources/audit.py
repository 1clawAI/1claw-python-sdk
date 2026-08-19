"""Audit resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class AuditResource:
    """Immutable audit event log."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        *,
        action: str | None = None,
        actor_id: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> OneclawResponse[Any]:
        """Query the audit trail with optional filters."""
        query: dict[str, Any] = {}
        for key, val in {
            "action": action, "actor_id": actor_id,
            "resource_type": resource_type, "resource_id": resource_id,
            "limit": limit, "offset": offset,
        }.items():
            if val is not None:
                query[key] = val
        return self._http.request("GET", "/v1/audit", query=query or None)

    def verify(
        self,
        *,
        from_time: str | None = None,
        to_time: str | None = None,
        limit: int | None = None,
    ) -> OneclawResponse[Any]:
        """Verify audit hash chain integrity for the calling organization."""
        query: dict[str, Any] = {}
        if from_time is not None:
            query["from"] = from_time
        if to_time is not None:
            query["to"] = to_time
        if limit is not None:
            query["limit"] = limit
        return self._http.request("GET", "/v1/audit/verify", query=query or None)
