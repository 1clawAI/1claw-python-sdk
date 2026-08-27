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

    def update_template(self, app_id: str, template_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Update a platform template."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request(
            "PATCH", f"/v1/platform/apps/{app_id}/templates/{template_id}", body=body,
        )

    def delete_template(self, app_id: str, template_id: str) -> OneclawResponse[Any]:
        """Delete a platform template."""
        return self._http.request(
            "DELETE", f"/v1/platform/apps/{app_id}/templates/{template_id}",
        )

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
        *,
        parameters: dict[str, Any] | None = None,
        return_to: str | None = None,
    ) -> OneclawResponse[Any]:
        """Bootstrap resources for a connected user from a template."""
        body: dict[str, Any] = {}
        if template_id:
            body["template_id"] = template_id
        if parameters is not None:
            body["parameters"] = parameters
        if return_to:
            body["return_to"] = return_to
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

    # -- Grants ----------------------------------------------------------------

    def grant_resources(self, connection_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Grant platform access to user resources."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request(
            "POST", f"/v1/platform/connections/{connection_id}/grant", body=body,
        )

    def list_grants(self, connection_id: str) -> OneclawResponse[Any]:
        """List grants for a connection."""
        return self._http.request("GET", f"/v1/platform/connections/{connection_id}/grants")

    def revoke_grant(self, connection_id: str, grant_id: str) -> OneclawResponse[Any]:
        """Revoke a specific grant."""
        return self._http.request(
            "DELETE", f"/v1/platform/connections/{connection_id}/grants/{grant_id}",
        )

    # -- Spend policies --------------------------------------------------------

    def create_spend_policy(self, app_id: str, **kwargs: Any) -> OneclawResponse[Any]:
        """Create an app-level default spend policy."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        return self._http.request("POST", f"/v1/platform/apps/{app_id}/spend-policies", body=body)

    def list_spend_policies(self, app_id: str) -> OneclawResponse[Any]:
        """List active spend policies for an app."""
        return self._http.request("GET", f"/v1/platform/apps/{app_id}/spend-policies")

    def set_user_spend_policy(
        self,
        connection_id: str,
        *,
        idempotency_key: str | None = None,
        **kwargs: Any,
    ) -> OneclawResponse[Any]:
        """Set a per-user spend policy override."""
        body = {k: v for k, v in kwargs.items() if v is not None}
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        return self._http.request(
            "PUT",
            f"/v1/platform/connections/{connection_id}/spend-policy",
            body=body,
            headers=headers,
        )

    def get_spend_policy(self, app_id: str, policy_id: str) -> OneclawResponse[Any]:
        """Get a spend policy by ID."""
        return self._http.request(
            "GET", f"/v1/platform/apps/{app_id}/spend-policies/{policy_id}",
        )

    def get_connection_spend_policy(self, connection_id: str) -> OneclawResponse[Any]:
        """Get effective spend policy for a connection (plt_ auth)."""
        return self._http.request(
            "GET", f"/v1/platform/connections/{connection_id}/spend-policy",
        )

    def delete_spend_policy(self, app_id: str, policy_id: str) -> OneclawResponse[Any]:
        """Deactivate a spend policy."""
        return self._http.request(
            "DELETE", f"/v1/platform/apps/{app_id}/spend-policies/{policy_id}",
        )

    # -- Marketplace & stats ---------------------------------------------------

    def marketplace(
        self,
        *,
        page: int | None = None,
        per_page: int | None = None,
        q: str | None = None,
        category: str | None = None,
    ) -> OneclawResponse[Any]:
        """Browse the public platform marketplace (no auth required).

        Parameters
        ----------
        page : int, optional
            Page number for pagination.
        per_page : int, optional
            Results per page.
        q : str, optional
            Free-text search query.
        category : str, optional
            Filter by app category.
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        if q is not None:
            params["q"] = q
        if category is not None:
            params["category"] = category
        return self._http.request(
            "GET", "/v1/platform/marketplace", query=params or None, skip_auth=True,
        )

    def get_app_stats(self, app_id: str) -> OneclawResponse[Any]:
        """Get aggregate statistics for a platform app.

        Returns connection counts, bootstrap totals, and grant summaries.

        Parameters
        ----------
        app_id : str
            The platform app UUID.
        """
        return self._http.request("GET", f"/v1/platform/apps/{app_id}/stats")

    def rotate_webhook_secret(self, app_id: str) -> OneclawResponse[Any]:
        """Rotate a platform app's webhook signing secret.

        Returns the new secret (shown only once).

        Parameters
        ----------
        app_id : str
            The platform app UUID.
        """
        return self._http.request(
            "POST", f"/v1/platform/apps/{app_id}/rotate-webhook-secret",
        )

    # -- Platform API expansion (v0.57) --------------------------------------

    def siwe_challenge(self, domain: str | None = None) -> OneclawResponse[Any]:
        """Issue a SIWE nonce for wallet-native user provisioning."""
        body: dict[str, Any] = {}
        if domain:
            body["domain"] = domain
        return self._http.request("POST", "/v1/platform/siwe/challenge", body=body or None)

    def get_connection(self, connection_id: str) -> OneclawResponse[Any]:
        """Get connection details including claim and entitlement status."""
        return self._http.request("GET", f"/v1/platform/connections/{connection_id}")

    def get_connection_usage(self, connection_id: str) -> OneclawResponse[Any]:
        """Get per-connection inference spend for the current UTC month."""
        return self._http.request("GET", f"/v1/platform/connections/{connection_id}/usage")

    def list_entitlements(self, connection_id: str) -> OneclawResponse[Any]:
        """List on-chain entitlement evaluations for a connection."""
        return self._http.request("GET", f"/v1/platform/connections/{connection_id}/entitlements")

    def refresh_entitlements(self, connection_id: str) -> OneclawResponse[Any]:
        """Trigger an immediate entitlement monitor refresh."""
        return self._http.request(
            "POST", f"/v1/platform/connections/{connection_id}/entitlements/refresh",
        )

    def preview_template(
        self,
        app_id: str,
        template_id: str,
        *,
        parameters: dict[str, Any] | None = None,
        subject: dict[str, Any] | None = None,
    ) -> OneclawResponse[Any]:
        """Preview resolved template spec with parameter substitution."""
        body: dict[str, Any] = {}
        if parameters is not None:
            body["parameters"] = parameters
        if subject is not None:
            body["subject"] = subject
        return self._http.request(
            "POST",
            f"/v1/platform/apps/{app_id}/templates/{template_id}/preview",
            body=body or None,
        )

    # -- Platform control plane (v0.58) --------------------------------------

    def transfer_app_ownership(
        self,
        app_id: str,
        *,
        target_org_id: str | None = None,
        target_user_email: str | None = None,
        confirm_token: str | None = None,
    ) -> OneclawResponse[Any]:
        """Transfer app ownership to another org (step-up via X-Auth-Confirm)."""
        body: dict[str, Any] = {}
        if target_org_id:
            body["target_org_id"] = target_org_id
        if target_user_email:
            body["target_user_email"] = target_user_email
        headers = {"X-Auth-Confirm": confirm_token} if confirm_token else None
        return self._http.request(
            "POST",
            f"/v1/platform/apps/{app_id}/transfer-ownership",
            body=body or None,
            headers=headers,
        )

    def list_connection_approvals(
        self,
        connection_id: str,
        *,
        status: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> OneclawResponse[Any]:
        """List approvals for a connected user (plt_ auth)."""
        query: dict[str, Any] = {}
        if status is not None:
            query["status"] = status
        if limit is not None:
            query["limit"] = limit
        if offset is not None:
            query["offset"] = offset
        return self._http.request(
            "GET",
            f"/v1/platform/connections/{connection_id}/approvals",
            query=query or None,
        )

    def get_connection_approval(
        self, connection_id: str, approval_id: str,
    ) -> OneclawResponse[Any]:
        """Get a single approval for a connection (plt_ auth)."""
        return self._http.request(
            "GET",
            f"/v1/platform/connections/{connection_id}/approvals/{approval_id}",
        )

    def list_connection_pending_approvals(
        self,
        connection_id: str,
        *,
        status: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> OneclawResponse[Any]:
        """List consensus pending approvals with payload_hash (plt_ auth)."""
        query: dict[str, Any] = {}
        if status is not None:
            query["status"] = status
        if limit is not None:
            query["limit"] = limit
        if offset is not None:
            query["offset"] = offset
        return self._http.request(
            "GET",
            f"/v1/platform/connections/{connection_id}/pending-approvals",
            query=query or None,
        )

    def get_template(self, app_id: str, template_id: str) -> OneclawResponse[Any]:
        """Get a bootstrap template by ID."""
        return self._http.request(
            "GET", f"/v1/platform/apps/{app_id}/templates/{template_id}",
        )

    def create_connection_runtime(
        self, connection_id: str, body: dict[str, Any],
    ) -> OneclawResponse[Any]:
        """Create a Cloud Runtime for a connection agent (plt_ auth)."""
        return self._http.request(
            "POST", f"/v1/platform/connections/{connection_id}/runtimes", body=body,
        )

    def connection_agent_chat(
        self, connection_id: str, agent_id: str, body: dict[str, Any],
    ) -> OneclawResponse[Any]:
        """Chat with an agent on a platform connection (plt_ auth)."""
        return self._http.request(
            "POST",
            f"/v1/platform/connections/{connection_id}/agents/{agent_id}/chat",
            body=body,
        )

    def decide_connection_pending_approval(
        self, connection_id: str, approval_id: str, body: dict[str, Any],
    ) -> OneclawResponse[Any]:
        """Vote on a consensus pending approval (plt_ auth)."""
        return self._http.request(
            "POST",
            f"/v1/platform/connections/{connection_id}/pending-approvals/{approval_id}/decide",
            body=body,
        )

    def decide_connection_approval(
        self, connection_id: str, approval_id: str, body: dict[str, Any],
    ) -> OneclawResponse[Any]:
        """Decide a mobile approval for a connection (plt_ auth)."""
        return self._http.request(
            "POST",
            f"/v1/platform/connections/{connection_id}/approvals/{approval_id}/decide",
            body=body,
        )

    def deactivate_connection_signing_key(
        self, connection_id: str, chain: str, *, agent_id: str | None = None,
    ) -> OneclawResponse[Any]:
        """Deactivate a signing key for a connection agent (plt_ auth)."""
        query = {"agent_id": agent_id} if agent_id else None
        return self._http.request(
            "DELETE",
            f"/v1/platform/connections/{connection_id}/signing-keys/{chain}",
            query=query,
        )

    def list_connection_signing_keys(
        self, connection_id: str, *, agent_id: str | None = None,
    ) -> OneclawResponse[Any]:
        """List signing keys for a connection agent (plt_ auth, public metadata only)."""
        query = {"agent_id": agent_id} if agent_id else None
        return self._http.request(
            "GET",
            f"/v1/platform/connections/{connection_id}/signing-keys",
            query=query,
        )

    def get_connection_signing_key(
        self, connection_id: str, chain: str, *, agent_id: str | None = None,
    ) -> OneclawResponse[Any]:
        """Get a signing key for a connection agent by chain (plt_ auth)."""
        query = {"agent_id": agent_id} if agent_id else None
        return self._http.request(
            "GET",
            f"/v1/platform/connections/{connection_id}/signing-keys/{chain}",
            query=query,
        )

    def patch_connection_agent(
        self,
        connection_id: str,
        agent_id: str,
        body: dict[str, Any],
    ) -> OneclawResponse[Any]:
        """Patch limited agent settings on a connection (plt_ auth)."""
        return self._http.request(
            "PATCH",
            f"/v1/platform/connections/{connection_id}/agents/{agent_id}",
            body=body,
        )

    def create_connection_pending_approval(
        self, connection_id: str, body: dict[str, Any],
    ) -> OneclawResponse[Any]:
        """Create a consensus pending approval for a connection agent (plt_ auth)."""
        return self._http.request(
            "POST",
            f"/v1/platform/connections/{connection_id}/pending-approvals",
            body=body,
        )

    def get_connection_portfolio(
        self,
        connection_id: str,
        *,
        chains: str | None = None,
        include_tokens: bool | None = None,
    ) -> OneclawResponse[Any]:
        """Portfolio/balances for connection agents (plt_ auth)."""
        query: dict[str, Any] = {}
        if chains is not None:
            query["chains"] = chains
        if include_tokens is not None:
            query["include_tokens"] = include_tokens
        return self._http.request(
            "GET",
            f"/v1/platform/connections/{connection_id}/portfolio",
            query=query or None,
        )

    def list_connection_automations(
        self, connection_id: str,
    ) -> OneclawResponse[Any]:
        """List automations for agents on a connection (plt_ auth)."""
        return self._http.request(
            "GET",
            f"/v1/platform/connections/{connection_id}/automations",
        )

    def create_connection_automation(
        self, connection_id: str, body: dict[str, Any],
    ) -> OneclawResponse[Any]:
        """Create automation for a connection agent (plt_ auth)."""
        return self._http.request(
            "POST",
            f"/v1/platform/connections/{connection_id}/automations",
            body=body,
        )

    def get_connection_memory(
        self,
        connection_id: str,
        namespace: str,
        key: str,
        *,
        agent_id: str | None = None,
    ) -> OneclawResponse[Any]:
        """Get agent memory on a connection (plt_ auth)."""
        query = {"agent_id": agent_id} if agent_id else None
        return self._http.request(
            "GET",
            f"/v1/platform/connections/{connection_id}/memory/{namespace}/{key}",
            query=query,
        )

    def put_connection_memory(
        self,
        connection_id: str,
        namespace: str,
        key: str,
        body: dict[str, Any],
        *,
        agent_id: str | None = None,
    ) -> OneclawResponse[Any]:
        """Upsert agent memory on a connection (plt_ auth)."""
        query = {"agent_id": agent_id} if agent_id else None
        return self._http.request(
            "PUT",
            f"/v1/platform/connections/{connection_id}/memory/{namespace}/{key}",
            body=body,
            query=query,
        )

    def delete_connection_memory(
        self,
        connection_id: str,
        namespace: str,
        key: str,
        *,
        agent_id: str | None = None,
    ) -> OneclawResponse[Any]:
        """Delete agent memory on a connection (plt_ auth)."""
        query = {"agent_id": agent_id} if agent_id else None
        return self._http.request(
            "DELETE",
            f"/v1/platform/connections/{connection_id}/memory/{namespace}/{key}",
            query=query,
        )

    def get_connection_runtime(
        self, connection_id: str, runtime_id: str,
    ) -> OneclawResponse[Any]:
        """Get a Cloud Runtime provisioned on a connection (plt_ auth)."""
        return self._http.request(
            "GET",
            f"/v1/platform/connections/{connection_id}/runtimes/{runtime_id}",
        )

    def connection_passkey_enroll_begin(
        self, connection_id: str,
    ) -> OneclawResponse[Any]:
        """Begin WebAuthn passkey enrollment for a connected end-user (plt_ auth)."""
        return self._http.request(
            "POST",
            f"/v1/platform/connections/{connection_id}/passkeys/enroll/begin",
        )

    def connection_passkey_enroll_complete(
        self, connection_id: str, body: dict[str, Any],
    ) -> OneclawResponse[Any]:
        """Complete WebAuthn passkey enrollment for a connected end-user (plt_ auth)."""
        return self._http.request(
            "POST",
            f"/v1/platform/connections/{connection_id}/passkeys/enroll/complete",
            body=body,
        )

    def get_platform_webhooks(self, app_id: str) -> OneclawResponse[Any]:
        """Platform webhook delivery catalog (plt_ or user JWT)."""
        return self._http.request("GET", f"/v1/platform/apps/{app_id}/webhooks")

    def inspect_content(
        self, content: str, *, context: str | None = None,
    ) -> OneclawResponse[Any]:
        """Scan text for threats (MCP inspect_content REST parity). Fail-closed."""
        body: dict[str, Any] = {"content": content}
        if context is not None:
            body["context"] = context
        return self._http.request("POST", "/v1/shroud/inspect-content", body=body)
