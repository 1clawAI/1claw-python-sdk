"""Discovery resource — agent directory and inter-agent communication."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class DiscoveryResource:
    """Agent discovery, org directory, and inter-agent task delegation."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_agent_card(self, agent_id: str) -> OneclawResponse[Any]:
        """Get an agent's public discovery card (no auth required)."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/card", skip_auth=True)

    def directory(
        self,
        *,
        query: str | None = None,
        tags: list[str] | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> OneclawResponse[Any]:
        """Search the public agent directory."""
        params: dict[str, Any] = {}
        if query is not None:
            params["q"] = query
        if tags is not None:
            params["tags"] = ",".join(tags)
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        return self._http.request(
            "GET", "/v1/agents/directory", query=params or None, skip_auth=True
        )

    def org_directory(
        self,
        *,
        query: str | None = None,
        tags: list[str] | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> OneclawResponse[Any]:
        """List agents in the caller's organization for sub-agent discovery."""
        params: dict[str, Any] = {}
        if query is not None:
            params["q"] = query
        if tags is not None:
            params["tags"] = ",".join(tags)
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["page_size"] = page_size
        return self._http.request("GET", "/v1/agents/org-directory", query=params or None)

    def update_discovery(self, agent_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Update an agent's discovery settings (human-only)."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("PATCH", f"/v1/agents/{agent_id}/discovery", body=body)

    def marketplace(
        self,
        *,
        query: str | None = None,
        category: str | None = None,
    ) -> OneclawResponse[Any]:
        """Search the platform marketplace."""
        params: dict[str, Any] = {}
        if query is not None:
            params["q"] = query
        if category is not None:
            params["category"] = category
        return self._http.request(
            "GET", "/v1/platform/marketplace", query=params or None, skip_auth=True
        )

    def delegate_task(
        self,
        agent_id: str,
        *,
        message: str,
        model: str | None = None,
        provider: str | None = None,
    ) -> OneclawResponse[Any]:
        """Send a task to another agent via chat (inter-agent communication)."""
        body: dict[str, Any] = {"message": message, "mode": "llm"}
        if model is not None:
            body["model"] = model
        if provider is not None:
            body["provider"] = provider
        return self._http.request("POST", f"/v1/agents/{agent_id}/chat", body=body)
