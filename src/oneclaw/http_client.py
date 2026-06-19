"""Internal HTTP transport for the 1Claw Python SDK."""

from __future__ import annotations

import base64
import json
import threading
import time
from typing import Any, TypeVar

import httpx

from oneclaw.errors import OneclawError, error_from_response
from oneclaw.types import ErrorInfo, OneclawClientConfig, OneclawResponse, ResponseMeta

T = TypeVar("T")

_REFRESH_BUFFER_SECS = 60


class HttpClient:
    """Low-level HTTP client that handles authentication and error mapping.

    All resource modules delegate requests through this class.
    Agent ``ocv_`` API keys are automatically exchanged for JWTs and
    refreshed 60 seconds before expiry.
    """

    def __init__(self, config: OneclawClientConfig) -> None:
        self._base_url = config.base_url.rstrip("/")
        self._token = config.token
        self._token_expires_at: float = 0
        self._timeout = config.timeout

        self._agent_credentials: dict[str, str | None] | None = None
        self._resolved_agent_id: str | None = None
        self._refresh_lock = threading.Lock()

        is_agent_key = (config.api_key or "").startswith("ocv_") or config.agent_id is not None
        if config.api_key and is_agent_key:
            self._agent_credentials = {
                "agent_id": config.agent_id,
                "api_key": config.api_key,
            }

        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=self._timeout,
            headers={"Content-Type": "application/json"},
        )

    # -- public helpers --------------------------------------------------------

    @property
    def resolved_agent_id(self) -> str | None:
        if self._resolved_agent_id:
            return self._resolved_agent_id
        if self._agent_credentials:
            return self._agent_credentials.get("agent_id")
        return None

    def set_token(self, token: str) -> None:
        self._token = token
        self._token_expires_at = self._decode_expiry(token)

    def get_token(self) -> str | None:
        return self._token

    @property
    def base_url(self) -> str:
        return self._base_url

    # -- request methods -------------------------------------------------------

    def request(
        self,
        method: str,
        path: str,
        *,
        body: Any | None = None,
        query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        skip_auth: bool = False,
    ) -> OneclawResponse[Any]:
        """Perform a typed request and return an :class:`OneclawResponse` envelope."""
        if not skip_auth:
            self._ensure_token()

        req_headers: dict[str, str] = {}
        if headers:
            req_headers.update(headers)
        if not skip_auth and self._token:
            req_headers["Authorization"] = f"Bearer {self._token}"

        cleaned_query = None
        if query:
            cleaned_query = {k: str(v) for k, v in query.items() if v is not None}

        try:
            response = self._client.request(
                method,
                path,
                json=body if body is not None else None,
                params=cleaned_query,
                headers=req_headers,
            )
        except httpx.HTTPError as exc:
            return OneclawResponse(
                data=None,
                error=ErrorInfo(type="network_error", message=str(exc)),
                meta=ResponseMeta(status=0),
            )

        if not response.is_success:
            try:
                err_body = response.json()
            except Exception:
                err_body = {}

            err = error_from_response(
                response.status_code,
                err_body if isinstance(err_body, dict) else {},
                dict(response.headers),
            )
            return OneclawResponse(
                data=None,
                error=ErrorInfo(type=err.error_type, message=str(err), detail=err.detail),
                meta=ResponseMeta(status=response.status_code),
            )

        if response.status_code == 204:
            return OneclawResponse(data=None, error=None, meta=ResponseMeta(status=204))

        return OneclawResponse(
            data=response.json(),
            error=None,
            meta=ResponseMeta(status=response.status_code),
        )

    def request_or_throw(
        self,
        method: str,
        path: str,
        *,
        body: Any | None = None,
        query: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        """Same as :meth:`request` but raises :class:`OneclawError` on failure."""
        self._ensure_token()

        req_headers: dict[str, str] = {}
        if headers:
            req_headers.update(headers)
        if self._token:
            req_headers["Authorization"] = f"Bearer {self._token}"

        cleaned_query = None
        if query:
            cleaned_query = {k: str(v) for k, v in query.items() if v is not None}

        response = self._client.request(
            method,
            path,
            json=body if body is not None else None,
            params=cleaned_query,
            headers=req_headers,
        )

        if not response.is_success:
            try:
                err_body = response.json()
            except Exception:
                err_body = {}
            raise error_from_response(
                response.status_code,
                err_body if isinstance(err_body, dict) else {},
                dict(response.headers),
            )

        if response.status_code == 204:
            return None

        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._client.close()

    # -- private helpers -------------------------------------------------------

    def _ensure_token(self) -> None:
        if not self._agent_credentials:
            return
        if self._token and time.time() < self._token_expires_at - _REFRESH_BUFFER_SECS:
            return

        with self._refresh_lock:
            if self._token and time.time() < self._token_expires_at - _REFRESH_BUFFER_SECS:
                return
            self._refresh_agent_token()

    def _refresh_agent_token(self) -> None:
        assert self._agent_credentials is not None
        payload: dict[str, Any] = {"api_key": self._agent_credentials["api_key"]}
        if self._agent_credentials.get("agent_id"):
            payload["agent_id"] = self._agent_credentials["agent_id"]

        response = self._client.post(
            "/v1/auth/agent-token",
            json=payload,
        )

        if not response.is_success:
            raise OneclawError(
                f"Agent token refresh failed: HTTP {response.status_code}",
                response.status_code,
                "auth_error",
            )

        data = response.json()
        self._token = data["access_token"]
        self._token_expires_at = time.time() + data.get("expires_in", 3600)

        if data.get("agent_id"):
            self._resolved_agent_id = data["agent_id"]
            if self._agent_credentials and not self._agent_credentials.get("agent_id"):
                self._agent_credentials["agent_id"] = data["agent_id"]

    @staticmethod
    def _decode_expiry(jwt: str) -> float:
        try:
            parts = jwt.split(".")
            if len(parts) != 3:
                return 0
            padding = 4 - len(parts[1]) % 4
            padded = parts[1] + "=" * padding
            payload = json.loads(base64.urlsafe_b64decode(padded))
            exp = payload.get("exp")
            return float(exp) if isinstance(exp, (int, float)) else 0
        except Exception:
            return 0
