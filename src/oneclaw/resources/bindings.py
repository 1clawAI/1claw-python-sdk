"""Execution Intents — bindings, execute, and execution history."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class BindingsResource:
    """Manage agent bindings and execute intents against external services."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        agent_id: str,
        *,
        name: str,
        binding_type: str,
        config: dict[str, Any] | None = None,
        guardrails: dict[str, Any] | None = None,
        credential: dict[str, Any] | None = None,
        credential_source: dict[str, Any] | None = None,
    ) -> OneclawResponse[Any]:
        """Create a binding for an agent."""
        body: dict[str, Any] = {"name": name, "binding_type": binding_type}
        for key, val in {
            "config": config,
            "guardrails": guardrails,
            "credential": credential,
            "credential_source": credential_source,
        }.items():
            if val is not None:
                body[key] = val
        return self._http.request("POST", f"/v1/agents/{agent_id}/bindings", body=body)

    def list(self, agent_id: str) -> OneclawResponse[Any]:
        """List all bindings for an agent."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/bindings")

    def get(self, agent_id: str, binding_id: str) -> OneclawResponse[Any]:
        """Get a binding by ID."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/bindings/{binding_id}")

    def update(
        self,
        agent_id: str,
        binding_id: str,
        **kwargs: Any,
    ) -> OneclawResponse[Any]:
        """Update a binding's configuration, guardrails, or active status."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request(
            "PATCH", f"/v1/agents/{agent_id}/bindings/{binding_id}", body=body,
        )

    def delete(self, agent_id: str, binding_id: str) -> OneclawResponse[Any]:
        """Delete a binding."""
        return self._http.request("DELETE", f"/v1/agents/{agent_id}/bindings/{binding_id}")

    def rotate_credential(
        self,
        agent_id: str,
        binding_id: str,
        *,
        credential: dict[str, Any],
    ) -> OneclawResponse[Any]:
        """Rotate (overwrite) a binding's stored credential."""
        return self._http.request(
            "POST",
            f"/v1/agents/{agent_id}/bindings/{binding_id}/rotate-credential",
            body={"credential": credential},
        )

    def test(
        self,
        agent_id: str,
        binding_id: str,
        *,
        timeout_ms: int | None = None,
    ) -> OneclawResponse[Any]:
        """Test connectivity of a binding."""
        body: dict[str, Any] = {}
        if timeout_ms is not None:
            body["timeout_ms"] = timeout_ms
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/bindings/{binding_id}/test", body=body,
        )

    def execute(
        self,
        agent_id: str,
        *,
        binding: str,
        intent_type: str,
        params: dict[str, Any] | None = None,
        execution_mode: str | None = None,
    ) -> OneclawResponse[Any]:
        """Execute an intent against a binding."""
        body: dict[str, Any] = {
            "binding": binding,
            "intent_type": intent_type,
            "params": params or {},
        }
        if execution_mode is not None:
            body["execution_mode"] = execution_mode
        return self._http.request("POST", f"/v1/agents/{agent_id}/execute", body=body)

    def list_executions(
        self,
        agent_id: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> OneclawResponse[Any]:
        """List execution events for an agent."""
        query: dict[str, Any] = {}
        if limit is not None:
            query["limit"] = limit
        if offset is not None:
            query["offset"] = offset
        return self._http.request(
            "GET", f"/v1/agents/{agent_id}/executions", query=query or None,
        )
