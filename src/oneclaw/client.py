"""Main client for the 1Claw Python SDK."""

from __future__ import annotations

from oneclaw.http_client import HttpClient
from oneclaw.resources.agents import AgentsResource
from oneclaw.resources.api_keys import ApiKeysResource
from oneclaw.resources.approvals import ApprovalsResource
from oneclaw.resources.audit import AuditResource
from oneclaw.resources.auth import AuthResource
from oneclaw.resources.billing import BillingResource
from oneclaw.resources.chains import ChainsResource
from oneclaw.resources.org import OrgResource
from oneclaw.resources.platform import PlatformResource
from oneclaw.resources.policies import PoliciesResource
from oneclaw.resources.risk import RiskResource
from oneclaw.resources.secrets import SecretsResource
from oneclaw.resources.sharing import SharingResource
from oneclaw.resources.signing_keys import SigningKeysResource
from oneclaw.resources.treasury import TreasuryResource
from oneclaw.resources.treasury_wallets import TreasuryWalletsResource
from oneclaw.resources.vaults import VaultResource
from oneclaw.resources.webhooks import WebhooksResource
from oneclaw.types import OneclawClientConfig


class OneclawClient:
    """The main 1Claw SDK client.

    All API resources are exposed as namespaced attributes for
    discoverability.

    Examples
    --------
    >>> from oneclaw import create_client
    >>>
    >>> # Agent with API key (auto-exchanges for JWT)
    >>> client = create_client(api_key="ocv_...")
    >>>
    >>> # Pre-authenticated with JWT
    >>> client = create_client(token="eyJ...")
    >>>
    >>> # Use resources
    >>> vaults = client.vaults.list()
    >>> secret = client.secrets.get(vault_id, "my-key")
    """

    def __init__(self, config: OneclawClientConfig) -> None:
        self._http = HttpClient(config)

        if (
            config.api_key
            and not config.token
            and not config.agent_id
            and not config.api_key.startswith("ocv_")
        ):
            self._auto_authenticate_user_key(config.api_key)

        self.auth = AuthResource(self._http)
        self.vaults = VaultResource(self._http)
        self.secrets = SecretsResource(self._http)
        self.agents = AgentsResource(self._http)
        self.policies = PoliciesResource(self._http)
        self.chains = ChainsResource(self._http)
        self.sharing = SharingResource(self._http)
        self.billing = BillingResource(self._http)
        self.audit = AuditResource(self._http)
        self.org = OrgResource(self._http)
        self.api_keys = ApiKeysResource(self._http)
        self.signing_keys = SigningKeysResource(self._http)
        self.treasury = TreasuryResource(self._http)
        self.treasury_wallets = TreasuryWalletsResource(self._http)
        self.platform = PlatformResource(self._http)
        self.approvals = ApprovalsResource(self._http)
        self.webhooks = WebhooksResource(self._http)
        self.risk = RiskResource(self._http)

    def _auto_authenticate_user_key(self, api_key: str) -> None:
        """Exchange a ``1ck_`` user API key for a JWT (fire-and-forget)."""
        try:
            resp = self._http.request(
                "POST", "/v1/auth/api-key-token",
                body={"api_key": api_key},
                skip_auth=True,
            )
            if resp.data and resp.data.get("access_token"):
                self._http.set_token(resp.data["access_token"])
        except Exception:
            pass

    @property
    def resolved_agent_id(self) -> str | None:
        """Agent ID resolved from the token exchange (for key-only auth)."""
        return self._http.resolved_agent_id

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> OneclawClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


def create_client(
    *,
    base_url: str = "https://api.1claw.xyz",
    token: str | None = None,
    api_key: str | None = None,
    agent_id: str | None = None,
    timeout: float = 30.0,
) -> OneclawClient:
    """Create a new 1Claw SDK client.

    Parameters
    ----------
    base_url : str
        The 1Claw API base URL (default: ``https://api.1claw.xyz``).
    token : str, optional
        A pre-existing JWT to use for authentication.
    api_key : str, optional
        An API key (``ocv_`` for agents, ``1ck_`` for users).
        Agent keys auto-exchange for JWTs and refresh before expiry.
    agent_id : str, optional
        The agent UUID (optional with ``ocv_`` keys — auto-discovered).
    timeout : float
        HTTP request timeout in seconds (default: 30).

    Returns
    -------
    OneclawClient
        A fully configured client instance.

    Examples
    --------
    >>> client = create_client(api_key="ocv_abc123")
    >>> vaults = client.vaults.list()
    """
    config = OneclawClientConfig(
        base_url=base_url,
        token=token,
        api_key=api_key,
        agent_id=agent_id,
        timeout=timeout,
    )
    return OneclawClient(config)
