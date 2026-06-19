"""Official Python SDK for the 1Claw secrets management platform."""

from oneclaw.client import OneclawClient, create_client
from oneclaw.errors import (
    ApprovalRequiredError,
    AuthError,
    NotFoundError,
    OneclawError,
    PaymentRequiredError,
    RateLimitError,
    ResourceLimitExceededError,
    ServerError,
    ValidationError,
)
from oneclaw.types import OneclawClientConfig, OneclawResponse

__version__ = "0.1.0"

__all__ = [
    "OneclawClient",
    "create_client",
    "OneclawClientConfig",
    "OneclawResponse",
    "OneclawError",
    "AuthError",
    "NotFoundError",
    "PaymentRequiredError",
    "RateLimitError",
    "ResourceLimitExceededError",
    "ValidationError",
    "ServerError",
    "ApprovalRequiredError",
]
