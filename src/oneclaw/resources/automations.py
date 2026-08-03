"""Automations resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse

WorkflowSpec = dict[str, Any] | Sequence[Any]


class AutomationsResource:
    """Scheduled, event-driven, and webhook-triggered agent workflows."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        *,
        name: str,
        agent_id: str,
        trigger_type: str,
        workflow_spec: WorkflowSpec,
        cron_expr: str | None = None,
        timezone: str = "UTC",
        event_filter: dict[str, Any] | None = None,
    ) -> OneclawResponse[Any]:
        """Create a new automation.

        ``workflow_spec`` is required: either a step array or ``{"steps": [...]}``.
        For cron triggers, pass ``cron_expr``. ``trigger_type="schedule"`` is
        accepted by the API and normalized to ``cron``.
        """
        body: dict[str, Any] = {
            "name": name,
            "agent_id": agent_id,
            "trigger_type": trigger_type,
            "timezone": timezone,
            "workflow_spec": workflow_spec,
        }
        if cron_expr is not None:
            body["cron_expr"] = cron_expr
        if event_filter is not None:
            body["event_filter"] = event_filter
        return self._http.request("POST", "/v1/automations", body=body)

    def list(self) -> OneclawResponse[Any]:
        """List automations for the current organization."""
        return self._http.request("GET", "/v1/automations")

    def get(self, automation_id: str) -> OneclawResponse[Any]:
        """Get a specific automation."""
        return self._http.request("GET", f"/v1/automations/{automation_id}")

    def update(
        self,
        automation_id: str,
        *,
        name: str | None = None,
        cron_expr: str | None = None,
        timezone: str | None = None,
        event_filter: dict[str, Any] | None = None,
        workflow_spec: WorkflowSpec | None = None,
        is_active: bool | None = None,
    ) -> OneclawResponse[Any]:
        """Update an existing automation."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if cron_expr is not None:
            body["cron_expr"] = cron_expr
        if timezone is not None:
            body["timezone"] = timezone
        if event_filter is not None:
            body["event_filter"] = event_filter
        if workflow_spec is not None:
            body["workflow_spec"] = workflow_spec
        if is_active is not None:
            body["is_active"] = is_active
        return self._http.request("PATCH", f"/v1/automations/{automation_id}", body=body)

    def delete(self, automation_id: str) -> OneclawResponse[Any]:
        """Delete an automation."""
        return self._http.request("DELETE", f"/v1/automations/{automation_id}")

    def list_runs(
        self, automation_id: str, *, limit: int | None = None
    ) -> OneclawResponse[Any]:
        """List recent runs for an automation."""
        query: dict[str, Any] | None = {"limit": limit} if limit else None
        return self._http.request(
            "GET", f"/v1/automations/{automation_id}/runs", query=query
        )

    def trigger(
        self, automation_id: str, *, input: dict[str, Any] | None = None
    ) -> OneclawResponse[Any]:
        """Manually trigger an automation run."""
        body: dict[str, Any] = {}
        if input is not None:
            body["input"] = input
        return self._http.request(
            "POST", f"/v1/automations/{automation_id}/trigger", body=body
        )
