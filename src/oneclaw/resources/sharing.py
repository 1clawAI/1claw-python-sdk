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
        secret_id: str,
        *,
        recipient_type: str,
        expires_at: str,
        recipient_id: str | None = None,
        email: str | None = None,
        permissions: list[str] | None = None,
        max_access_count: int | None = None,
        passphrase: str | None = None,
        ip_allowlist: list[str] | None = None,
    ) -> OneclawResponse[Any]:
        """Share a secret (``POST /v1/secrets/{secret_id}/share``).

        ``recipient_type`` is one of ``user``, ``agent``, ``external_email``,
        ``anyone_with_link`` or ``creator``. ``expires_at`` is an RFC 3339
        timestamp. ``email`` is required for ``external_email``;
        ``recipient_id`` for ``user`` and ``agent``.
        """
        body: dict[str, Any] = {
            "recipient_type": recipient_type,
            "expires_at": expires_at,
        }
        for key, val in {
            "recipient_id": recipient_id,
            "email": email,
            "permissions": permissions,
            "max_access_count": max_access_count,
            "passphrase": passphrase,
            "ip_allowlist": ip_allowlist,
        }.items():
            if val is not None:
                body[key] = val
        return self._http.request("POST", f"/v1/secrets/{secret_id}/share", body=body)

    def list_outbound(self) -> OneclawResponse[Any]:
        """List shares created by the current identity."""
        return self._http.request("GET", "/v1/shares/outbound")

    def list_inbound(self) -> OneclawResponse[Any]:
        """List shares received by the current identity."""
        return self._http.request("GET", "/v1/shares/inbound")

    def accept(self, share_id: str) -> OneclawResponse[Any]:
        """Accept an inbound share."""
        return self._http.request("POST", f"/v1/shares/{share_id}/accept")

    def decline(self, share_id: str) -> OneclawResponse[Any]:
        """Decline an inbound share."""
        return self._http.request("POST", f"/v1/shares/{share_id}/decline")

    def revoke(self, share_id: str) -> OneclawResponse[Any]:
        """Revoke a share link you created (``DELETE /v1/share/{share_id}``)."""
        return self._http.request("DELETE", f"/v1/share/{share_id}")

    def delete(self, share_id: str) -> OneclawResponse[Any]:
        """Alias of :meth:`revoke`."""
        return self.revoke(share_id)

    def access(self, share_id: str, passphrase: str | None = None) -> OneclawResponse[Any]:
        """Read a shared secret (``GET /v1/share/{share_id}``).

        Link shares need no auth. Shares targeted at a user or agent need the
        recipient's token, which is sent when the client has one. The
        passphrase goes in the request body, never the query string.
        """
        body: dict[str, Any] | None = None
        if passphrase:
            body = {"passphrase": passphrase}
        return self._http.request("GET", f"/v1/share/{share_id}", body=body)
