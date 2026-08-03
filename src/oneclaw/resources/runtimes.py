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
        template: str | None = None,
        preset: str | None = None,
        image: str | None = None,
        env_public: dict[str, str] | None = None,
        idle_timeout_secs: int | None = None,
        expose_http: bool | None = None,
        http_port: int | None = None,
        slug: str | None = None,
        inbound_auth: str | None = None,
        shell_access_enabled: bool | None = None,
        shell_auth_policy: str | None = None,
        shell_max_session_minutes: int | None = None,
    ) -> OneclawResponse[Any]:
        """Create a new runtime deployment."""
        body: dict[str, Any] = {
            "agent_id": agent_id,
            "name": name,
        }
        if template is not None:
            body["template"] = template
        if preset is not None:
            body["preset"] = preset
        if image is not None:
            body["image"] = image
        if env_public is not None:
            body["env_public"] = env_public
        if idle_timeout_secs is not None:
            body["idle_timeout_secs"] = idle_timeout_secs
        if expose_http is not None:
            body["expose_http"] = expose_http
        if http_port is not None:
            body["http_port"] = http_port
        if slug is not None:
            body["slug"] = slug
        if inbound_auth is not None:
            body["inbound_auth"] = inbound_auth
        if shell_access_enabled is not None:
            body["shell_access_enabled"] = shell_access_enabled
        if shell_auth_policy is not None:
            body["shell_auth_policy"] = shell_auth_policy
        if shell_max_session_minutes is not None:
            body["shell_max_session_minutes"] = shell_max_session_minutes
        return self._http.request("POST", "/v1/runtimes", body=body)

    def list(self) -> OneclawResponse[Any]:
        """List runtimes for the current organization."""
        return self._http.request("GET", "/v1/runtimes")

    def get(self, runtime_id: str) -> OneclawResponse[Any]:
        """Get a runtime by ID."""
        return self._http.request("GET", f"/v1/runtimes/{runtime_id}")

    def update(
        self,
        runtime_id: str,
        *,
        name: str | None = None,
        image: str | None = None,
        env_public: dict[str, str] | None = None,
        idle_timeout_secs: int | None = None,
        expose_http: bool | None = None,
        http_port: int | None = None,
        slug: str | None = None,
        inbound_auth: str | None = None,
        shell_access_enabled: bool | None = None,
        shell_auth_policy: str | None = None,
        shell_max_session_minutes: int | None = None,
    ) -> OneclawResponse[Any]:
        """Update a runtime deployment."""
        body: dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if image is not None:
            body["image"] = image
        if env_public is not None:
            body["env_public"] = env_public
        if idle_timeout_secs is not None:
            body["idle_timeout_secs"] = idle_timeout_secs
        if expose_http is not None:
            body["expose_http"] = expose_http
        if http_port is not None:
            body["http_port"] = http_port
        if slug is not None:
            body["slug"] = slug
        if inbound_auth is not None:
            body["inbound_auth"] = inbound_auth
        if shell_access_enabled is not None:
            body["shell_access_enabled"] = shell_access_enabled
        if shell_auth_policy is not None:
            body["shell_auth_policy"] = shell_auth_policy
        if shell_max_session_minutes is not None:
            body["shell_max_session_minutes"] = shell_max_session_minutes
        return self._http.request("PATCH", f"/v1/runtimes/{runtime_id}", body=body)

    def delete(self, runtime_id: str) -> OneclawResponse[Any]:
        """Delete a runtime deployment."""
        return self._http.request("DELETE", f"/v1/runtimes/{runtime_id}")

    def start(self, runtime_id: str) -> OneclawResponse[Any]:
        """Start a stopped runtime."""
        return self._http.request("POST", f"/v1/runtimes/{runtime_id}/start")

    def stop(self, runtime_id: str) -> OneclawResponse[Any]:
        """Stop a running runtime."""
        return self._http.request("POST", f"/v1/runtimes/{runtime_id}/stop")

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

    def create_shell_session(
        self,
        runtime_id: str,
        *,
        password: str | None = None,
        totp_code: str | None = None,
        passkey_credential: dict[str, Any] | None = None,
        reauth_token: str | None = None,
    ) -> OneclawResponse[Any]:
        """Create an interactive shell WebSocket session (human-only, step-up auth)."""
        body: dict[str, Any] = {}
        if password is not None:
            body["password"] = password
        if totp_code is not None:
            body["totp_code"] = totp_code
        if passkey_credential is not None:
            body["passkey_credential"] = passkey_credential
        if reauth_token is not None:
            body["reauth_token"] = reauth_token
        return self._http.request(
            "POST", f"/v1/runtimes/{runtime_id}/shell/session", body=body
        )
