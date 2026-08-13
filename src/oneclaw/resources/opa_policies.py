"""OPA policies resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class OpaPoliciesResource:
    """OPA (Open Policy Agent) policy management for the organization."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        *,
        rego_module: str,
        description: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> OneclawResponse[Any]:
        """Create an OPA policy (Rego module)."""
        body: dict[str, Any] = {"rego_module": rego_module}
        if description is not None:
            body["description"] = description
        if data is not None:
            body["data"] = data
        return self._http.request("POST", "/v1/org/opa-policies", body=body)

    def list(self) -> OneclawResponse[Any]:
        """List all OPA policies for the organization."""
        return self._http.request("GET", "/v1/org/opa-policies")

    def get(self, policy_id: str) -> OneclawResponse[Any]:
        """Get an OPA policy by ID."""
        return self._http.request("GET", f"/v1/org/opa-policies/{policy_id}")

    def delete(self, policy_id: str) -> OneclawResponse[Any]:
        """Delete an OPA policy."""
        return self._http.request("DELETE", f"/v1/org/opa-policies/{policy_id}")

    def test(
        self, *, input: dict[str, Any], data: dict[str, Any] | None = None
    ) -> OneclawResponse[Any]:
        """Evaluate an OPA policy against test input."""
        body: dict[str, Any] = {"input": input}
        if data is not None:
            body["data"] = data
        return self._http.request("POST", "/v1/org/opa-policies/test", body=body)
