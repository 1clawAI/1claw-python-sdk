"""Channels resource — external messaging channels for agents."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class ChannelsResource:
    """Manage external messaging channels (Telegram, WhatsApp, Discord) for agents."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        agent_id: str,
        channel_type: str,
        *,
        channel_name: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> OneclawResponse[Any]:
        """Register a new messaging channel for an agent (human-only).

        Parameters
        ----------
        agent_id : str
            The agent UUID.
        channel_type : str
            One of ``telegram``, ``whatsapp``, ``discord``.
        channel_name : str, optional
            Human-friendly name for the channel.
        config : dict, optional
            Channel-specific configuration (bot token, webhook secret, etc.).
        """
        body: dict[str, Any] = {"channel_type": channel_type}
        if channel_name is not None:
            body["channel_name"] = channel_name
        if config is not None:
            body["config"] = config
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/channels", body=body
        )

    def list(self, agent_id: str) -> OneclawResponse[Any]:
        """List all messaging channels for an agent."""
        return self._http.request("GET", f"/v1/agents/{agent_id}/channels")

    def get(self, agent_id: str, channel_id: str) -> OneclawResponse[Any]:
        """Get a specific channel."""
        return self._http.request(
            "GET", f"/v1/agents/{agent_id}/channels/{channel_id}"
        )

    def update(
        self,
        agent_id: str,
        channel_id: str,
        *,
        channel_name: str | None = None,
        is_active: bool | None = None,
        config: dict[str, Any] | None = None,
    ) -> OneclawResponse[Any]:
        """Update a channel's name, active status, or config (human-only)."""
        body: dict[str, Any] = {}
        if channel_name is not None:
            body["channel_name"] = channel_name
        if is_active is not None:
            body["is_active"] = is_active
        if config is not None:
            body["config"] = config
        return self._http.request(
            "PATCH", f"/v1/agents/{agent_id}/channels/{channel_id}", body=body
        )

    def delete(self, agent_id: str, channel_id: str) -> OneclawResponse[Any]:
        """Delete a messaging channel (human-only)."""
        return self._http.request(
            "DELETE", f"/v1/agents/{agent_id}/channels/{channel_id}"
        )

    def send_message(
        self,
        agent_id: str,
        channel_id: str,
        *,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> OneclawResponse[Any]:
        """Send an outbound message via a registered channel."""
        body: dict[str, Any] = {"content": content}
        if metadata is not None:
            body["metadata"] = metadata
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/channels/{channel_id}/send", body=body
        )

    def list_messages(
        self,
        agent_id: str,
        channel_id: str,
        *,
        limit: int | None = None,
        offset: int | None = None,
    ) -> OneclawResponse[Any]:
        """List inbound and outbound messages for a channel."""
        query: dict[str, Any] = {}
        if limit is not None:
            query["limit"] = limit
        if offset is not None:
            query["offset"] = offset
        return self._http.request(
            "GET",
            f"/v1/agents/{agent_id}/channels/{channel_id}/messages",
            query=query or None,
        )
