"""Cedar policies resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class CedarPoliciesResource:
    """Cedar policy management for the organization."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self, *, name: str, cedar_text: str
    ) -> OneclawResponse[Any]:
        """Create a Cedar policy."""
        return self._http.request(
            "POST",
            "/v1/org/cedar-policies",
            body={"name": name, "cedar_text": cedar_text},
        )

    def list(self) -> OneclawResponse[Any]:
        """List all Cedar policies for the organization."""
        return self._http.request("GET", "/v1/org/cedar-policies")

    def get(self, policy_id: str) -> OneclawResponse[Any]:
        """Get a Cedar policy by ID."""
        return self._http.request("GET", f"/v1/org/cedar-policies/{policy_id}")

    def delete(self, policy_id: str) -> OneclawResponse[Any]:
        """Delete a Cedar policy."""
        return self._http.request("DELETE", f"/v1/org/cedar-policies/{policy_id}")

    def test(
        self,
        *,
        principal: str,
        action: str,
        resource: str,
        context: dict[str, Any] | None = None,
    ) -> OneclawResponse[Any]:
        """Test a Cedar authorization decision."""
        body: dict[str, Any] = {"principal": principal, "action": action, "resource": resource}
        if context is not None:
            body["context"] = context
        return self._http.request("POST", "/v1/org/cedar-policies/test", body=body)
