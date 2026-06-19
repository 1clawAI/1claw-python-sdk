"""Chains resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class ChainsResource:
    """Supported blockchains — list chains and query details."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> OneclawResponse[Any]:
        """List all enabled blockchain networks."""
        return self._http.request("GET", "/v1/chains")

    def get(self, identifier: str) -> OneclawResponse[Any]:
        """Get chain details by name or chain ID."""
        return self._http.request("GET", f"/v1/chains/{identifier}")
