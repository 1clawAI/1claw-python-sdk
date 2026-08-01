"""Automations resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class AutomationsResource:
    """Cron-based scheduled tasks for agents."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        agent_id: str,
        *,
        name: str,
        schedule: str,
        action_type: str,
        action_config: dict[str, Any],
        description: str | None = None,
        enabled: bool = True,
    ) -> OneclawResponse[Any]:
        """Create a new automation for an agent."""
        body: dict[str, Any] = {
            "name": name,
            "schedule": schedule,
            "action_type": action_type,
            "action_config": action_config,
            "enabled": enabled,
        }
        if description is not None:
            body["description"] = description
        return self._http.request("POST", f"/v1/agents/{agent_id}/automations", body=body)

    def list(self, agent_id: str) -> OneclawResponse[Any]:
        """List automations for an agent."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/automations")

    def get(self, agent_id: str, automation_id: str) -> OneclawResponse[Any]:
        """Get a specific automation."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/automations/{automation_id}")

    def update(
        self,
        agent_id: str,
        automation_id: str,
        *,
        name: str | None = None,
        schedule: str | None = None,
        action_config: dict[str, Any] | None = None,
        enabled: bool | None = None,
    ) -> OneclawResponse[Any]:
        """Update an existing automation."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if schedule is not None:
            body["schedule"] = schedule
        if action_config is not None:
            body["action_config"] = action_config
        if enabled is not None:
            body["enabled"] = enabled
        return self._http.request(
            "PATCH", f"/v1/agents/{agent_id}/automations/{automation_id}", body=body
        )

    def delete(self, agent_id: str, automation_id: str) -> OneclawResponse[Any]:
        """Delete an automation."""
        return self._http.request(
            "DELETE", f"/v1/agents/{agent_id}/automations/{automation_id}"
        )

    def list_runs(
        self, agent_id: str, automation_id: str, *, limit: int | None = None
    ) -> OneclawResponse[Any]:
        """List recent runs for an automation."""
        query: dict[str, Any] | None = {"limit": limit} if limit else None
        return self._http.request(
            "GET", f"/v1/agents/{agent_id}/automations/{automation_id}/runs", query=query
        )

    def trigger(self, agent_id: str, automation_id: str) -> OneclawResponse[Any]:
        """Manually trigger an automation run."""
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/automations/{automation_id}/trigger"
        )
