"""Sub-organizations resource."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class SubOrgsResource:
    """Sub-organization management."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        billing_model: str = "inherit",
    ) -> OneclawResponse[Any]:
        """Create a sub-organization."""
        body: dict[str, Any] = {"name": name, "billing_model": billing_model}
        if description is not None:
            body["description"] = description
        return self._http.request("POST", "/v1/org/sub-orgs", body=body)

    def list(self) -> OneclawResponse[Any]:
        """List all sub-organizations."""
        return self._http.request("GET", "/v1/org/sub-orgs")

    def get(self, sub_org_id: str) -> OneclawResponse[Any]:
        """Get a sub-organization by ID."""
        return self._http.request("GET", f"/v1/org/sub-orgs/{sub_org_id}")

    def archive(self, sub_org_id: str) -> OneclawResponse[Any]:
        """Archive a sub-organization."""
        return self._http.request("DELETE", f"/v1/org/sub-orgs/{sub_org_id}")

    def grant_permission(
        self,
        sub_org_id: str,
        *,
        permission: str,
        resource_ids: builtins.list[str] | None = None,
    ) -> OneclawResponse[Any]:
        """Grant a permission to a sub-organization."""
        body: dict[str, Any] = {"permission": permission}
        if resource_ids is not None:
            body["resource_ids"] = resource_ids
        return self._http.request("POST", f"/v1/org/sub-orgs/{sub_org_id}/permissions", body=body)

    def revoke_permission(self, sub_org_id: str, permission_id: str) -> OneclawResponse[Any]:
        """Revoke a permission from a sub-organization."""
        return self._http.request(
            "DELETE", f"/v1/org/sub-orgs/{sub_org_id}/permissions/{permission_id}"
        )

    def add_user(
        self, sub_org_id: str, *, user_id: str, role: str = "member"
    ) -> OneclawResponse[Any]:
        """Add a user to a sub-organization."""
        return self._http.request(
            "POST",
            f"/v1/org/sub-orgs/{sub_org_id}/users",
            body={"user_id": user_id, "role": role},
        )

    def generate_wallets(
        self, sub_org_id: str, *, chains: builtins.list[str] | None = None
    ) -> OneclawResponse[Any]:
        """Generate treasury wallets for a sub-organization."""
        body: dict[str, Any] = {}
        if chains is not None:
            body["chains"] = chains
        return self._http.request(
            "POST", f"/v1/org/sub-orgs/{sub_org_id}/wallets/generate", body=body
        )
