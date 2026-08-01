"""Runtimes resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class RuntimesResource:
    """Managed runtime environments for agents."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        *,
        agent_id: str,
        name: str,
        image: str,
        env: dict[str, str] | None = None,
        cpu: str | None = None,
        memory_mb: int | None = None,
        replicas: int | None = None,
        health_check_path: str | None = None,
    ) -> OneclawResponse[Any]:
        """Create a new runtime deployment."""
        body: dict[str, Any] = {
            "agent_id": agent_id,
            "name": name,
            "image": image,
        }
        if env is not None:
            body["env"] = env
        if cpu is not None:
            body["cpu"] = cpu
        if memory_mb is not None:
            body["memory_mb"] = memory_mb
        if replicas is not None:
            body["replicas"] = replicas
        if health_check_path is not None:
            body["health_check_path"] = health_check_path
        return self._http.request("POST", "/v1/runtimes", body=body)

    def list(self, *, agent_id: str | None = None) -> OneclawResponse[Any]:
        """List runtimes, optionally filtered by agent."""
        query: dict[str, Any] | None = {"agent_id": agent_id} if agent_id else None
        return self._http.request("GET", "/v1/runtimes", query=query)

    def get(self, runtime_id: str) -> OneclawResponse[Any]:
        """Get a runtime by ID."""
        return self._http.request("GET", f"/v1/runtimes/{runtime_id}")

    def update(
        self,
        runtime_id: str,
        *,
        image: str | None = None,
        env: dict[str, str] | None = None,
        replicas: int | None = None,
        status: str | None = None,
    ) -> OneclawResponse[Any]:
        """Update a runtime deployment."""
        body: dict[str, Any] = {}
        if image is not None:
            body["image"] = image
        if env is not None:
            body["env"] = env
        if replicas is not None:
            body["replicas"] = replicas
        if status is not None:
            body["status"] = status
        return self._http.request("PATCH", f"/v1/runtimes/{runtime_id}", body=body)

    def delete(self, runtime_id: str) -> OneclawResponse[Any]:
        """Delete a runtime deployment."""
        return self._http.request("DELETE", f"/v1/runtimes/{runtime_id}")

    def logs(
        self, runtime_id: str, *, since: str | None = None, limit: int | None = None
    ) -> OneclawResponse[Any]:
        """Get runtime logs."""
        query: dict[str, Any] = {}
        if since is not None:
            query["since"] = since
        if limit is not None:
            query["limit"] = limit
        return self._http.request("GET", f"/v1/runtimes/{runtime_id}/logs", query=query or None)

    def restart(self, runtime_id: str) -> OneclawResponse[Any]:
        """Restart a runtime."""
        return self._http.request("POST", f"/v1/runtimes/{runtime_id}/restart")
