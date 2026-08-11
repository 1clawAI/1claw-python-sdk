"""OAuth Connected Accounts — manage OAuth provider connections for agents."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class OAuthConnectResource:
    """Manage OAuth provider connections for agents."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_providers(self) -> OneclawResponse[Any]:
        """List all available OAuth providers in the registry."""
        return self._http.request("GET", "/v1/oauth/providers")

    def list_connections(self, agent_id: str) -> OneclawResponse[Any]:
        """List all OAuth connections for an agent."""
        return self._http.request(
            "GET", f"/v1/agents/{agent_id}/oauth/connections"
        )

    def connect(
        self,
        agent_id: str,
        provider_slug: str,
        *,
        scopes: list[str] | None = None,
        redirect_after: str | None = None,
    ) -> OneclawResponse[Any]:
        """Initiate an OAuth connection for an agent.

        Parameters
        ----------
        agent_id : str
            The agent UUID.
        provider_slug : str
            The OAuth provider slug (e.g. ``github``, ``google``).
        scopes : list[str], optional
            OAuth scopes to request.
        redirect_after : str, optional
            URL to redirect to after the OAuth flow completes.
        """
        body: dict[str, Any] = {"provider_slug": provider_slug}
        if scopes is not None:
            body["scopes"] = scopes
        if redirect_after is not None:
            body["redirect_after"] = redirect_after
        return self._http.request(
            "POST", f"/v1/agents/{agent_id}/oauth/connect", body=body
        )

    def disconnect(
        self, agent_id: str, binding_id: str
    ) -> OneclawResponse[Any]:
        """Disconnect (revoke) an OAuth connection for an agent."""
        return self._http.request(
            "POST",
            f"/v1/agents/{agent_id}/oauth/disconnect/{binding_id}",
        )

    def save_app_credentials(
        self,
        agent_id: str,
        provider_slug: str,
        *,
        client_id: str,
        client_secret: str,
        redirect_uri: str | None = None,
    ) -> OneclawResponse[Any]:
        """Save custom OAuth app credentials for a provider.

        Parameters
        ----------
        agent_id : str
            The agent UUID.
        provider_slug : str
            The OAuth provider slug.
        client_id : str
            OAuth client ID.
        client_secret : str
            OAuth client secret.
        redirect_uri : str, optional
            Custom redirect URI for the OAuth flow.
        """
        body: dict[str, Any] = {
            "provider_slug": provider_slug,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if redirect_uri is not None:
            body["redirect_uri"] = redirect_uri
        return self._http.request(
            "POST",
            f"/v1/agents/{agent_id}/oauth/app-credentials",
            body=body,
        )

    def list_app_credentials(self, agent_id: str) -> OneclawResponse[Any]:
        """List saved OAuth app credentials for an agent."""
        return self._http.request(
            "GET", f"/v1/agents/{agent_id}/oauth/app-credentials"
        )

    def delete_app_credentials(
        self, agent_id: str, provider_slug: str
    ) -> OneclawResponse[Any]:
        """Delete saved OAuth app credentials for a provider."""
        return self._http.request(
            "DELETE",
            f"/v1/agents/{agent_id}/oauth/app-credentials/{provider_slug}",
        )
