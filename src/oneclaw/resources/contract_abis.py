"""Contract ABI registry resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class ContractAbisResource:
    """Org-scoped contract ABI registry for transaction decoding."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def create(
        self,
        *,
        chain: str,
        contract_address: str,
        abi_json: list[dict[str, Any]],
        name: str | None = None,
        description: str | None = None,
        token_decimals: int | None = None,
    ) -> OneclawResponse[Any]:
        """Register a contract ABI."""
        body: dict[str, Any] = {
            "chain": chain,
            "contract_address": contract_address,
            "abi_json": abi_json,
        }
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if token_decimals is not None:
            body["token_decimals"] = token_decimals
        return self._http.request("POST", "/v1/org/contract-abis", body=body)

    def list(self, *, chain: str | None = None) -> OneclawResponse[Any]:
        """List contract ABIs, optionally filtered by chain."""
        params = {"chain": chain} if chain else None
        return self._http.request("GET", "/v1/org/contract-abis", query=params)

    def get(self, abi_id: str) -> OneclawResponse[Any]:
        """Get a contract ABI by ID."""
        return self._http.request("GET", f"/v1/org/contract-abis/{abi_id}")

    def delete(self, abi_id: str) -> OneclawResponse[Any]:
        """Delete a contract ABI."""
        return self._http.request("DELETE", f"/v1/org/contract-abis/{abi_id}")
