"""Secret sharing resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class SharingResource:
    """Secret sharing — create time-limited share links."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        *,
        vault_id: str,
        secret_path: str,
        expires_in_hours: int = 24,
        max_views: int | None = None,
        passphrase: str | None = None,
        recipient_type: str | None = None,
        recipient_email: str | None = None,
        ip_allowlist: list[str] | None = None,
    ) -> OneclawResponse[Any]:
        """Create a share link for a secret."""
        body: dict[str, Any] = {
            "vault_id": vault_id,
            "secret_path": secret_path,
            "expires_in_hours": expires_in_hours,
        }
        for key, val in {
            "max_views": max_views, "passphrase": passphrase,
            "recipient_type": recipient_type, "recipient_email": recipient_email,
            "ip_allowlist": ip_allowlist,
        }.items():
            if val is not None:
                body[key] = val
        return self._http.request("POST", "/v1/shares", body=body)

    def list_outbound(self) -> OneclawResponse[Any]:
        """List shares created by the current identity."""
        return self._http.request("GET", "/v1/shares")

    def list_inbound(self) -> OneclawResponse[Any]:
        """List shares received by the current identity."""
        return self._http.request("GET", "/v1/shares/inbound")

    def get(self, share_id: str) -> OneclawResponse[Any]:
        """Get a share by ID."""
        return self._http.request("GET", f"/v1/shares/{share_id}")

    def accept(self, share_id: str) -> OneclawResponse[Any]:
        """Accept an inbound share."""
        return self._http.request("POST", f"/v1/shares/{share_id}/accept")

    def decline(self, share_id: str) -> OneclawResponse[Any]:
        """Decline an inbound share."""
        return self._http.request("POST", f"/v1/shares/{share_id}/decline")

    def delete(self, share_id: str) -> OneclawResponse[Any]:
        """Delete/revoke a share link."""
        return self._http.request("DELETE", f"/v1/shares/{share_id}")

    def access(self, share_id: str, passphrase: str | None = None) -> OneclawResponse[Any]:
        """Access a shared secret (public, uses share token auth)."""
        body: dict[str, Any] | None = None
        if passphrase:
            body = {"passphrase": passphrase}
        return self._http.request(
            "POST", f"/v1/shares/{share_id}/access",
            body=body, skip_auth=True,
        )
