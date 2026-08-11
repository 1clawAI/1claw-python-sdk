"""Agent Memory resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class MemoryResource:
    """Three-tier memory (scratch / durable / semantic) for agents."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def put(
        self,
        agent_id: str,
        namespace: str,
        key: str,
        *,
        value: str,
        tier: str = "durable",
        ttl_secs: int | None = None,
    ) -> OneclawResponse[Any]:
        """Store or upsert a memory entry."""
        body: dict[str, Any] = {"value": value, "tier": tier}
        if ttl_secs is not None:
            body["ttl_secs"] = ttl_secs
        return self._http.request(
            "PUT", f"/v1/agents/{agent_id}/memory/{namespace}/{key}", body=body,
        )

    # Legacy alias
    store = put

    def get(self, agent_id: str, namespace: str, key: str) -> OneclawResponse[Any]:
        """Get a specific memory entry."""
        return self._http.request(
            "GET", f"/v1/agents/{agent_id}/memory/{namespace}/{key}",
        )

    def delete(self, agent_id: str, namespace: str, key: str) -> OneclawResponse[Any]:
        """Delete a memory entry."""
        return self._http.request(
            "DELETE", f"/v1/agents/{agent_id}/memory/{namespace}/{key}",
        )

    def list(self, agent_id: str, namespace: str) -> OneclawResponse[Any]:
        """List entries in a namespace."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/memory/{namespace}")

    def list_namespaces(self, agent_id: str) -> OneclawResponse[Any]:
        """List namespaces for an agent."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/memory")

    def search(
        self,
        agent_id: str,
        *,
        namespace: str,
        query: str,
        top_k: int | None = None,
    ) -> OneclawResponse[Any]:
        """Semantic search over agent memory."""
        body: dict[str, Any] = {"namespace": namespace, "query": query}
        if top_k is not None:
            body["top_k"] = top_k
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/memory/search", body=body,
        )

    def delete_namespace(self, agent_id: str, namespace: str) -> OneclawResponse[Any]:
        """Delete an entire namespace."""
        return self._http.request(
            "DELETE", f"/v1/agents/{agent_id}/memory/{namespace}",
        )
