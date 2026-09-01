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

# Single source of truth: the version lives in pyproject.toml and is read
# from the installed distribution metadata. A hand-maintained literal here
# drifts the moment a release bumps one and not the other — 0.59.8 shipped
# reporting 0.59.6, so anyone checking __version__ got the wrong answer.
try:  # pragma: no cover - trivial
    from importlib.metadata import PackageNotFoundError, version as _dist_version

    __version__ = _dist_version("oneclaw")
except PackageNotFoundError:  # running from a source tree, not installed
    __version__ = "0+unknown"
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
