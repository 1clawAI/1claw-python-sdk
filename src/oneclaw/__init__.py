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
from oneclaw.resources.cedar_policies import CedarPoliciesResource
from oneclaw.resources.opa_policies import OpaPoliciesResource
from oneclaw.resources.portfolio import PortfolioResource
from oneclaw.resources.sub_orgs import SubOrgsResource
from oneclaw.types import CredentialSource, OneclawClientConfig, OneclawResponse

__version__ = "0.48.2"

__all__ = [
    "OneclawClient",
    "create_client",
    "CedarPoliciesResource",
    "OpaPoliciesResource",
    "PortfolioResource",
    "SubOrgsResource",
    "CredentialSource",
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
