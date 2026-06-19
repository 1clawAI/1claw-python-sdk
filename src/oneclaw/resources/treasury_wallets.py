"""Treasury wallets resource."""

from __future__ import annotations

import builtins
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class TreasuryWalletsResource:
    """Multi-chain wallet generation for human users."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def generate(self, chains: builtins.list[str] | None = None) -> OneclawResponse[Any]:
        """Generate wallets for specified chains (or all 6 if omitted)."""
        body: dict[str, Any] = {}
        if chains:
            body["chains"] = chains
        return self._http.request("POST", "/v1/treasury/wallets/generate", body=body)

    def list(self) -> OneclawResponse[Any]:
        """List all active wallets for the calling user."""
        return self._http.request("GET", "/v1/treasury/wallets")

    def get(self, chain: str) -> OneclawResponse[Any]:
        """Get wallet for a specific chain."""
        return self._http.request("GET", f"/v1/treasury/wallets/{chain}")

    def balance(self, chain: str) -> OneclawResponse[Any]:
        """Get native + ERC-20 token balances for a wallet."""
        return self._http.request("GET", f"/v1/treasury/wallets/{chain}/balance")

    def send(
        self,
        chain: str,
        *,
        to: str,
        value: str,
        password: str,
        data: str | None = None,
        gasless: bool | None = None,
        token_address: str | None = None,
    ) -> OneclawResponse[Any]:
        """Send native currency or ERC-20 tokens (requires password re-auth)."""
        body: dict[str, Any] = {"to": to, "value": value}
        if data is not None:
            body["data"] = data
        if gasless is not None:
            body["gasless"] = gasless
        if token_address is not None:
            body["token_address"] = token_address
        return self._http.request(
            "POST", f"/v1/treasury/wallets/{chain}/send",
            body=body, headers={"X-Auth-Confirm": password},
        )

    def swap(
        self,
        chain: str,
        *,
        sell_token: str,
        buy_token: str,
        sell_amount: str,
        password: str,
    ) -> OneclawResponse[Any]:
        """Swap tokens via 0x DEX aggregator (requires password re-auth)."""
        return self._http.request(
            "POST", f"/v1/treasury/wallets/{chain}/swap",
            body={
                "sell_token": sell_token,
                "buy_token": buy_token,
                "sell_amount": sell_amount,
            },
            headers={"X-Auth-Confirm": password},
        )

    def export(self, chain: str, password: str) -> OneclawResponse[Any]:
        """Export wallet with private key (requires password re-auth)."""
        return self._http.request(
            "POST", f"/v1/treasury/wallets/{chain}/export",
            headers={"X-Auth-Confirm": password},
        )

    def rotate(self, chain: str) -> OneclawResponse[Any]:
        """Rotate wallet keypair."""
        return self._http.request("POST", f"/v1/treasury/wallets/{chain}/rotate")

    def deactivate(self, chain: str) -> OneclawResponse[Any]:
        """Deactivate a wallet."""
        return self._http.request("DELETE", f"/v1/treasury/wallets/{chain}")

    def get_effective_spend_policy(self) -> OneclawResponse[Any]:
        """View the effective spend policy for the calling user."""
        return self._http.request("GET", "/v1/treasury/wallets/spend-policy")
