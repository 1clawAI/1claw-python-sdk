"""Platform API resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class PlatformResource:
    """Platform API — build multi-tenant apps on top of 1Claw."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    # -- Apps ------------------------------------------------------------------

    def create_app(
        self,
        name: str,
        slug: str,
        *,
        description: str | None = None,
        billing_model: str = "platform_pays",
        auth_mode: str = "silent",
        redirect_uris: list[str] | None = None,
        oidc_jwks_url: str | None = None,
        oidc_issuer: str | None = None,
        webhook_url: str | None = None,
        max_connected_users: int | None = None,
    ) -> OneclawResponse[Any]:
        """Register a new platform app. Returns the ``plt_`` API key once."""
        body: dict[str, Any] = {
            "name": name, "slug": slug,
            "billing_model": billing_model, "auth_mode": auth_mode,
        }
        for key, val in {
            "description": description, "redirect_uris": redirect_uris,
            "oidc_jwks_url": oidc_jwks_url, "oidc_issuer": oidc_issuer,
            "webhook_url": webhook_url, "max_connected_users": max_connected_users,
        }.items():
            if val is not None:
                body[key] = val
        return self._http.request("POST", "/v1/platform/apps", body=body)

    def list_apps(self) -> OneclawResponse[Any]:
        """List platform apps for the organization."""
        return self._http.request("GET", "/v1/platform/apps")

    def get_app(self, app_id: str) -> OneclawResponse[Any]:
        """Get a platform app by ID."""
        return self._http.request("GET", f"/v1/platform/apps/{app_id}")

    def update_app(self, app_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Update a platform app."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("PATCH", f"/v1/platform/apps/{app_id}", body=body)

    def delete_app(self, app_id: str) -> OneclawResponse[Any]:
        """Delete a platform app."""
        return self._http.request("DELETE", f"/v1/platform/apps/{app_id}")

    def rotate_key(
        self, app_id: str, api_key_expires_at: str | None = None
    ) -> OneclawResponse[Any]:
        """Rotate the platform app's API key."""
        body: dict[str, Any] = {}
        if api_key_expires_at:
            body["api_key_expires_at"] = api_key_expires_at
        return self._http.request(
            "POST", f"/v1/platform/apps/{app_id}/rotate-key", body=body or None,
        )

    # -- Templates -------------------------------------------------------------

    def create_template(
        self, app_id: str, name: str, spec: dict[str, Any], description: str | None = None
    ) -> OneclawResponse[Any]:
        """Create a bootstrap template."""
        body: dict[str, Any] = {"name": name, "spec": spec}
        if description:
            body["description"] = description
        return self._http.request("POST", f"/v1/platform/apps/{app_id}/templates", body=body)

    def list_templates(self, app_id: str) -> OneclawResponse[Any]:
        """List templates for a platform app."""
        return self._http.request("GET", f"/v1/platform/apps/{app_id}/templates")

    # -- User provisioning -----------------------------------------------------

    def upsert_user(
        self,
        *,
        email: str | None = None,
        subject_token: str | None = None,
    ) -> OneclawResponse[Any]:
        """Provision or find a user. Platform-only."""
        body: dict[str, Any] = {}
        if email:
            body["email"] = email
        if subject_token:
            body["subject_token"] = subject_token
        return self._http.request("POST", "/v1/platform/users/upsert", body=body)

    def bootstrap_user(
        self,
        connection_id: str,
        template_id: str | None = None,
    ) -> OneclawResponse[Any]:
        """Bootstrap resources for a connected user from a template."""
        body: dict[str, Any] = {}
        if template_id:
            body["template_id"] = template_id
        return self._http.request(
            "POST", f"/v1/platform/connections/{connection_id}/bootstrap", body=body,
        )

    def reissue_claim(self, connection_id: str) -> OneclawResponse[Any]:
        """Mint a fresh claim URL for an already-bootstrapped connection."""
        return self._http.request("POST", f"/v1/platform/connections/{connection_id}/reissue-claim")

    def list_connected_users(self, app_id: str) -> OneclawResponse[Any]:
        """List connected users for a platform app."""
        return self._http.request("GET", f"/v1/platform/apps/{app_id}/users")

    def app_audit(self, app_id: str) -> OneclawResponse[Any]:
        """Get platform audit events for an app."""
        return self._http.request("GET", f"/v1/platform/apps/{app_id}/audit")

    def list_connected_apps(self) -> OneclawResponse[Any]:
        """List apps connected to the calling user."""
        return self._http.request("GET", "/v1/platform/connected-apps")

    def disconnect_app(self, connection_id: str) -> OneclawResponse[Any]:
        """Disconnect from a platform app."""
        return self._http.request("DELETE", f"/v1/platform/connected-apps/{connection_id}")

    def claim_preview(self, token: str) -> OneclawResponse[Any]:
        """Preview a claim token (public)."""
        return self._http.request("GET", f"/v1/platform/claim/{token}", skip_auth=True)

    def claim_redeem(self, token: str) -> OneclawResponse[Any]:
        """Redeem a one-time claim token (public)."""
        return self._http.request("POST", f"/v1/platform/claim/{token}", skip_auth=True)

    # -- Spend policies --------------------------------------------------------

    def create_spend_policy(self, app_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Create an app-level default spend policy."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("POST", f"/v1/platform/apps/{app_id}/spend-policies", body=body)

    def list_spend_policies(self, app_id: str) -> OneclawResponse[Any]:
        """List active spend policies for an app."""
        return self._http.request("GET", f"/v1/platform/apps/{app_id}/spend-policies")

    def set_user_spend_policy(self, connection_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Set a per-user spend policy override."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request(
            "PUT", f"/v1/platform/connections/{connection_id}/spend-policy", body=body,
        )

    def delete_spend_policy(self, app_id: str, policy_id: str) -> OneclawResponse[Any]:
        """Deactivate a spend policy."""
        return self._http.request(
            "DELETE", f"/v1/platform/apps/{app_id}/spend-policies/{policy_id}",
        )
