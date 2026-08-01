"""Agent Memory resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class MemoryResource:
    """Persistent vector memory for agents."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def store(
        self,
        agent_id: str,
        *,
        content: str,
        metadata: dict[str, Any] | None = None,
        namespace: str | None = None,
    ) -> OneclawResponse[Any]:
        """Store a memory entry with automatic embedding."""
        body: dict[str, Any] = {"content": content}
        if metadata is not None:
            body["metadata"] = metadata
        if namespace is not None:
            body["namespace"] = namespace
        return self._http.request("POST", f"/v1/agents/{agent_id}/memory", body=body)

    def search(
        self,
        agent_id: str,
        *,
        query: str,
        limit: int | None = None,
        namespace: str | None = None,
        threshold: float | None = None,
    ) -> OneclawResponse[Any]:
        """Search memory entries by semantic similarity."""
        body: dict[str, Any] = {"query": query}
        if limit is not None:
            body["limit"] = limit
        if namespace is not None:
            body["namespace"] = namespace
        if threshold is not None:
            body["threshold"] = threshold
        return self._http.request("POST", f"/v1/agents/{agent_id}/memory/search", body=body)

    def list(
        self,
        agent_id: str,
        *,
        namespace: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> OneclawResponse[Any]:
        """List memory entries for an agent."""
        query: dict[str, Any] = {}
        if namespace is not None:
            query["namespace"] = namespace
        if limit is not None:
            query["limit"] = limit
        if offset is not None:
            query["offset"] = offset
        return self._http.request(
            "GET", f"/v1/agents/{agent_id}/memory", query=query or None
        )

    def get(self, agent_id: str, entry_id: str) -> OneclawResponse[Any]:
        """Get a specific memory entry."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/memory/{entry_id}")

    def delete(self, agent_id: str, entry_id: str) -> OneclawResponse[Any]:
        """Delete a memory entry."""
        return self._http.request("DELETE", f"/v1/agents/{agent_id}/memory/{entry_id}")

    def clear(self, agent_id: str, *, namespace: str | None = None) -> OneclawResponse[Any]:
        """Clear all memory entries for an agent (optionally within a namespace)."""
        body: dict[str, Any] = {}
        if namespace is not None:
            body["namespace"] = namespace
        return self._http.request("POST", f"/v1/agents/{agent_id}/memory/clear", body=body)
