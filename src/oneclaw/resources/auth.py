"""Authentication resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class AuthResource:
    """Authentication — login, agent auth, API key auth, signup, MFA."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def login(self, email: str, password: str) -> OneclawResponse[Any]:
        """Authenticate with email and password. Returns JWT or MFA challenge."""
        resp = self._http.request(
            "POST", "/v1/auth/token",
            body={"email": email, "password": password},
            skip_auth=True,
        )
        if resp.data and resp.data.get("access_token"):
            self._http.set_token(resp.data["access_token"])
        return resp

    def agent_token(
        self, api_key: str, agent_id: str | None = None
    ) -> OneclawResponse[Any]:
        """Exchange agent credentials for a JWT."""
        body: dict[str, Any] = {"api_key": api_key}
        if agent_id:
            body["agent_id"] = agent_id
        resp = self._http.request(
            "POST", "/v1/auth/agent-token", body=body, skip_auth=True,
        )
        if resp.data and resp.data.get("access_token"):
            self._http.set_token(resp.data["access_token"])
        return resp

    def api_key_token(self, api_key: str) -> OneclawResponse[Any]:
        """Exchange a user API key (``1ck_``) for a JWT."""
        resp = self._http.request(
            "POST", "/v1/auth/api-key-token",
            body={"api_key": api_key},
            skip_auth=True,
        )
        if resp.data and resp.data.get("access_token"):
            self._http.set_token(resp.data["access_token"])
        return resp

    def signup(
        self,
        email: str,
        password: str,
        display_name: str | None = None,
    ) -> OneclawResponse[Any]:
        """Register a new user account."""
        body: dict[str, Any] = {"email": email, "password": password}
        if display_name:
            body["display_name"] = display_name
        return self._http.request("POST", "/v1/auth/signup", body=body, skip_auth=True)

    def me(self) -> OneclawResponse[Any]:
        """Get the current user's profile."""
        return self._http.request("GET", "/v1/auth/me")

    def revoke_token(self) -> OneclawResponse[Any]:
        """Revoke the current Bearer token."""
        return self._http.request("DELETE", "/v1/auth/token")

    def refresh(self) -> OneclawResponse[Any]:
        """Refresh the current JWT."""
        resp = self._http.request("POST", "/v1/auth/refresh")
        if resp.data and resp.data.get("access_token"):
            self._http.set_token(resp.data["access_token"])
        return resp

    def change_password(self, current_password: str, new_password: str) -> OneclawResponse[Any]:
        """Change the current user's password."""
        return self._http.request(
            "POST", "/v1/auth/change-password",
            body={"current_password": current_password, "new_password": new_password},
        )

    def forgot_password(self, email: str) -> OneclawResponse[Any]:
        """Initiate a password reset."""
        return self._http.request(
            "POST", "/v1/auth/forgot-password",
            body={"email": email},
            skip_auth=True,
        )

    def reset_password(self, token: str, new_password: str) -> OneclawResponse[Any]:
        """Complete a password reset with the emailed token."""
        return self._http.request(
            "POST", "/v1/auth/reset-password",
            body={"token": token, "new_password": new_password},
            skip_auth=True,
        )

    def mfa_status(self) -> OneclawResponse[Any]:
        """Get MFA status for the current user."""
        return self._http.request("GET", "/v1/auth/mfa/status")

    def mfa_setup(self) -> OneclawResponse[Any]:
        """Begin MFA setup. Returns TOTP secret and provisioning URI."""
        return self._http.request("POST", "/v1/auth/mfa/setup")

    def mfa_verify_setup(self, code: str) -> OneclawResponse[Any]:
        """Verify TOTP code to complete MFA setup."""
        return self._http.request("POST", "/v1/auth/mfa/verify-setup", body={"code": code})

    def mfa_verify(self, mfa_token: str, code: str) -> OneclawResponse[Any]:
        """Verify MFA code during login. Returns the final JWT."""
        resp = self._http.request(
            "POST", "/v1/auth/mfa/verify",
            body={"mfa_token": mfa_token, "code": code},
            skip_auth=True,
        )
        if resp.data and resp.data.get("access_token"):
            self._http.set_token(resp.data["access_token"])
        return resp

    def mfa_disable(
        self, code: str | None = None, password: str | None = None
    ) -> OneclawResponse[Any]:
        """Disable MFA. Requires either a TOTP code or account password."""
        body: dict[str, Any] = {}
        if code:
            body["code"] = code
        if password:
            body["password"] = password
        return self._http.request("DELETE", "/v1/auth/mfa", body=body)

    def federated_token(
        self, audience: str, subject_token: str | None = None, scope: str | None = None
    ) -> OneclawResponse[Any]:
        """Exchange a 1Claw token for an RS256 OIDC JWT with a custom audience."""
        body: dict[str, Any] = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "audience": audience,
            "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        }
        if subject_token:
            body["subject_token"] = subject_token
        if scope:
            body["scope"] = scope
        return self._http.request("POST", "/v1/auth/federated-token", body=body)

    def export_data(self) -> OneclawResponse[Any]:
        """GDPR data export of the calling user's personal data."""
        return self._http.request("POST", "/v1/auth/export-data")

    def social_login(
        self,
        provider: str,
        id_token: str,
        oauth_redirect_uri: str | None = None,
        auto_provision_chains: list[str] | None = None,
    ) -> OneclawResponse[Any]:
        """Authenticate via social login (Google, Apple, Discord)."""
        body: dict[str, Any] = {"provider": provider, "id_token": id_token}
        if oauth_redirect_uri:
            body["oauth_redirect_uri"] = oauth_redirect_uri
        if auto_provision_chains:
            body["auto_provision_chains"] = auto_provision_chains
        return self._http.request("POST", "/v1/auth/social-login", body=body, skip_auth=True)

    def send_email_otp(
        self, email: str, platform_app_id: str | None = None
    ) -> OneclawResponse[Any]:
        """Send a one-time email code for passwordless login."""
        body: dict[str, Any] = {"email": email}
        if platform_app_id:
            body["platform_app_id"] = platform_app_id
        return self._http.request("POST", "/v1/auth/email-otp/send", body=body, skip_auth=True)

    def verify_email_otp(
        self,
        email: str,
        code: str,
        platform_app_id: str | None = None,
        auto_provision_chains: list[str] | None = None,
    ) -> OneclawResponse[Any]:
        """Verify email OTP code. Returns JWT on success."""
        body: dict[str, Any] = {"email": email, "code": code}
        if platform_app_id:
            body["platform_app_id"] = platform_app_id
        if auto_provision_chains:
            body["auto_provision_chains"] = auto_provision_chains
        resp = self._http.request(
            "POST", "/v1/auth/email-otp/verify", body=body, skip_auth=True,
        )
        if resp.data and resp.data.get("access_token"):
            self._http.set_token(resp.data["access_token"])
        return resp
