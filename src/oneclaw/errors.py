"""Error types for the 1Claw Python SDK."""

from __future__ import annotations

import contextlib
from typing import Any


class OneclawError(Exception):
    """Base error for all 1Claw SDK errors."""

    def __init__(
        self,
        message: str,
        status: int,
        error_type: str = "unknown",
        detail: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.error_type = error_type
        self.detail = detail


class AuthError(OneclawError):
    """Raised on 401 Unauthorized or 403 Forbidden responses."""

    def __init__(self, message: str, status: int = 401) -> None:
        super().__init__(message, status, "auth_error")


class ResourceLimitExceededError(OneclawError):
    """Raised when a resource limit is exceeded (403 with type resource_limit_exceeded)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, 403, "resource_limit_exceeded")


class PaymentRequiredError(OneclawError):
    """Raised on 402 Payment Required responses."""

    def __init__(self, message: str, requirement: dict[str, Any] | None = None) -> None:
        super().__init__(message, 402, "payment_required")
        self.payment_requirement = requirement


class ApprovalRequiredError(OneclawError):
    """Raised when human approval is needed to access a resource."""

    def __init__(self, approval_request_id: str, message: str | None = None) -> None:
        super().__init__(
            message or "Human approval is required to access this secret",
            403,
            "approval_required",
        )
        self.approval_request_id = approval_request_id


class NotFoundError(OneclawError):
    """Raised on 404 Not Found responses."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, 404, "not_found")


class RateLimitError(OneclawError):
    """Raised on 429 Too Many Requests. Includes retry timing when available."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after_ms: int | None = None,
    ) -> None:
        super().__init__(message, 429, "rate_limit")
        self.retry_after_ms = retry_after_ms


class ValidationError(OneclawError):
    """Raised on 400 Bad Request responses for validation failures."""

    def __init__(self, message: str, fields: dict[str, str] | None = None) -> None:
        super().__init__(message, 400, "validation_error")
        self.fields = fields


class ServerError(OneclawError):
    """Raised on 500+ server-side errors."""

    def __init__(self, message: str = "Internal server error", status: int = 500) -> None:
        super().__init__(message, status, "server_error")


def error_from_response(
    status: int,
    body: dict[str, Any],
    headers: dict[str, str] | None = None,
) -> OneclawError:
    """Parse an HTTP response into the appropriate typed error."""
    message = body.get("detail") or body.get("message") or body.get("error") or f"HTTP {status}"

    if status == 400:
        return ValidationError(message, body.get("fields"))
    if status == 401:
        return AuthError(message, 401)
    if status == 403:
        error_type = body.get("type", "")
        if error_type == "resource_limit_exceeded":
            return ResourceLimitExceededError(message)
        if error_type == "approval_required":
            return ApprovalRequiredError(body.get("approval_request_id", ""), message)
        return AuthError(message, 403)
    if status == 402:
        return PaymentRequiredError(message, body)
    if status == 404:
        return NotFoundError(message)
    if status == 429:
        retry_after_ms = None
        if headers and "retry-after" in headers:
            with contextlib.suppress(ValueError):
                retry_after_ms = int(headers["retry-after"]) * 1000
        return RateLimitError(message, retry_after_ms)
    if status >= 500:
        return ServerError(message, status)
    return OneclawError(message, status, "unknown")
