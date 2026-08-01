"""Discovery resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class DiscoveryResource:
    """Agent discovery and directory listing."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def publish(
        self,
        agent_id: str,
        *,
        description: str,
        tags: list[str] | None = None,
        category: str | None = None,
        website_url: str | None = None,
        is_public: bool = True,
    ) -> OneclawResponse[Any]:
        """Publish an agent to the discovery directory."""
        body: dict[str, Any] = {
            "description": description,
            "is_public": is_public,
        }
        if tags is not None:
            body["tags"] = tags
        if category is not None:
            body["category"] = category
        if website_url is not None:
            body["website_url"] = website_url
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/discovery", body=body
        )

    def unpublish(self, agent_id: str) -> OneclawResponse[Any]:
        """Remove an agent from the discovery directory."""
        return self._http.request("DELETE", f"/v1/agents/{agent_id}/discovery")

    def get_listing(self, agent_id: str) -> OneclawResponse[Any]:
        """Get the discovery listing for an agent."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/discovery")

    def update_listing(
        self,
        agent_id: str,
        *,
        description: str | None = None,
        tags: list[str] | None = None,
        category: str | None = None,
        is_public: bool | None = None,
    ) -> OneclawResponse[Any]:
        """Update an agent's discovery listing."""
        body: dict[str, Any] = {}
        if description is not None:
            body["description"] = description
        if tags is not None:
            body["tags"] = tags
        if category is not None:
            body["category"] = category
        if is_public is not None:
            body["is_public"] = is_public
        return self._http.request(
            "PATCH", f"/v1/agents/{agent_id}/discovery", body=body
        )

    def search(
        self,
        *,
        query: str | None = None,
        tags: list[str] | None = None,
        category: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> OneclawResponse[Any]:
        """Search the agent discovery directory."""
        params: dict[str, Any] = {}
        if query is not None:
            params["q"] = query
        if tags is not None:
            params["tags"] = ",".join(tags)
        if category is not None:
            params["category"] = category
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        return self._http.request("GET", "/v1/directory", query=params or None)
