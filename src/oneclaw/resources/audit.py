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
