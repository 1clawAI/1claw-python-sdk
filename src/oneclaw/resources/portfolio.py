"""Portfolio resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class PortfolioResource:
    """Aggregated portfolio view across all wallets."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get(
        self, *, chains: str | None = None, include_tokens: bool = False
    ) -> OneclawResponse[Any]:
        """Get an aggregated portfolio view."""
        params: dict[str, str] = {}
        if chains is not None:
            params["chains"] = chains
        if include_tokens:
            params["include_tokens"] = "true"
        return self._http.request("GET", "/v1/portfolio", query=params)
