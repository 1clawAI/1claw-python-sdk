"""Shared types for the 1Claw Python SDK."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass
class OneclawClientConfig:
    """Configuration for the 1Claw SDK client."""

    base_url: str = "https://api.1claw.xyz"
    token: str | None = None
    api_key: str | None = None
    agent_id: str | None = None
    timeout: float = 30.0


@dataclass
class ErrorInfo:
    type: str
    message: str
    detail: str | None = None


@dataclass
class ResponseMeta:
    status: int


@dataclass
class OneclawResponse(Generic[T]):
    """Envelope returned by every SDK method. Check ``error`` before using ``data``."""

    data: T | None
    error: ErrorInfo | None
    meta: ResponseMeta


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class LoginResponse:
    access_token: str | None = None
    expires_in: int | None = None
    user_id: str | None = None
    mfa_required: bool | None = None
    mfa_token: str | None = None


@dataclass
class TokenResponse:
    access_token: str
    expires_in: int
    agent_id: str | None = None
    vault_ids: list[str] | None = None


@dataclass
class AgentTokenRequest:
    api_key: str
    agent_id: str | None = None


@dataclass
class SignupRequest:
    email: str
    password: str
    display_name: str | None = None


@dataclass
class SignupResponse:
    user_id: str
    message: str | None = None


@dataclass
class UserProfile:
    id: str
    email: str
    display_name: str | None = None
    org_id: str | None = None
    role: str | None = None
    billing_tier: str | None = None
    wallet_address: str | None = None


# ---------------------------------------------------------------------------
# Vaults
# ---------------------------------------------------------------------------

@dataclass
class CreateVaultRequest:
    name: str
    description: str = ""
    mpc_custody: str | None = None


@dataclass
class VaultResponse:
    id: str
    name: str
    org_id: str
    description: str | None = None
    created_at: str | None = None
    created_by: str | None = None
    kek_id: str | None = None
    cmek_enabled: bool | None = None
    cmek_fingerprint: str | None = None
    mpc_custody: str | None = None
    mpc_threshold: int | None = None
    mpc_providers: list[str] | None = None
    platform_app_id: str | None = None
    platform_locked: bool | None = None


@dataclass
class VaultListResponse:
    vaults: list[VaultResponse] = field(default_factory=list)


@dataclass
class EnableCmekRequest:
    fingerprint: str


@dataclass
class EnableMpcRequest:
    custody_mode: str
    providers: list[str] | None = None


@dataclass
class CmekRotationJobResponse:
    job_id: str
    status: str
    total_secrets: int | None = None
    processed: int | None = None
    error: str | None = None


# ---------------------------------------------------------------------------
# Secrets
# ---------------------------------------------------------------------------

@dataclass
class PutSecretRequest:
    value: str
    type: str = "generic"
    metadata: dict[str, Any] | None = None
    expires_at: str | None = None
    rotation_policy: dict[str, Any] | None = None
    max_access_count: int | None = None


@dataclass
class SecretMetadataResponse:
    path: str
    version: int
    type: str | None = None
    created_at: str | None = None
    expires_at: str | None = None
    metadata: dict[str, Any] | None = None
    client_share: str | None = None
    cmek_encrypted: bool | None = None


@dataclass
class SecretResponse:
    path: str
    value: str
    version: int
    type: str | None = None
    created_at: str | None = None
    expires_at: str | None = None
    metadata: dict[str, Any] | None = None
    cmek_encrypted: bool | None = None


@dataclass
class SecretListResponse:
    secrets: list[SecretMetadataResponse] = field(default_factory=list)


@dataclass
class SecretVersionListResponse:
    versions: list[SecretMetadataResponse] = field(default_factory=list)


@dataclass
class RotateSecretRequest:
    length: int | None = None
    charset: str | None = None
    type: str | None = None


# ---------------------------------------------------------------------------
# Policies
# ---------------------------------------------------------------------------

@dataclass
class CreatePolicyRequest:
    principal_type: str
    principal_id: str
    secret_path_pattern: str
    permissions: list[str] = field(default_factory=lambda: ["read"])
    conditions: dict[str, Any] | None = None
    expires_at: str | None = None


@dataclass
class UpdatePolicyRequest:
    permissions: list[str] | None = None
    conditions: dict[str, Any] | None = None
    expires_at: str | None = None


@dataclass
class PolicyResponse:
    id: str
    vault_id: str
    principal_type: str
    principal_id: str
    secret_path_pattern: str
    permissions: list[str] = field(default_factory=list)
    conditions: dict[str, Any] | None = None
    expires_at: str | None = None
    created_at: str | None = None
    created_by: str | None = None
    platform_app_id: str | None = None


@dataclass
class PolicyListResponse:
    policies: list[PolicyResponse] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

@dataclass
class CreateAgentRequest:
    name: str
    description: str = ""
    auth_method: str = "api_key"
    intents_api_enabled: bool = False
    shroud_enabled: bool = False
    shroud_config: dict[str, Any] | None = None
    token_ttl_seconds: int | None = None
    vault_ids: list[str] | None = None
    scopes: list[str] | None = None
    tx_to_allowlist: list[str] | None = None
    tx_max_value_eth: str | None = None
    tx_daily_limit_eth: str | None = None
    tx_allowed_chains: list[str] | None = None
    federation_enabled: bool | None = None
    federation_audiences: list[str] | None = None
    message_signing_enabled: bool | None = None
    eip712_default_policy: str | None = None
    eip712_domain_allowlist: list[dict[str, Any]] | None = None
    api_key_expires_at: str | None = None


@dataclass
class UpdateAgentRequest:
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    intents_api_enabled: bool | None = None
    shroud_enabled: bool | None = None
    shroud_config: dict[str, Any] | None = None
    token_ttl_seconds: int | None = None
    vault_ids: list[str] | None = None
    scopes: list[str] | None = None
    tx_to_allowlist: list[str] | None = None
    tx_max_value_eth: str | None = None
    tx_daily_limit_eth: str | None = None
    tx_allowed_chains: list[str] | None = None
    federation_enabled: bool | None = None
    federation_audiences: list[str] | None = None
    message_signing_enabled: bool | None = None
    eip712_default_policy: str | None = None
    eip712_domain_allowlist: list[dict[str, Any]] | None = None
    api_key_expires_at: str | None = None


@dataclass
class AgentResponse:
    id: str
    name: str
    org_id: str
    description: str | None = None
    is_active: bool | None = None
    auth_method: str | None = None
    created_at: str | None = None
    created_by: str | None = None
    ssh_public_key: str | None = None
    ecdh_public_key: str | None = None
    intents_api_enabled: bool | None = None
    shroud_enabled: bool | None = None
    shroud_config: dict[str, Any] | None = None
    token_ttl_seconds: int | None = None
    vault_ids: list[str] | None = None
    scopes: list[str] | None = None
    signing_chains: list[str] | None = None
    tx_to_allowlist: list[str] | None = None
    tx_max_value_eth: str | None = None
    tx_daily_limit_eth: str | None = None
    tx_spent_today_eth: str | None = None
    tx_allowed_chains: list[str] | None = None
    evm_address: str | None = None
    smart_accounts: list[dict[str, Any]] | None = None
    federation_enabled: bool | None = None
    federation_audiences: list[str] | None = None
    message_signing_enabled: bool | None = None
    eip712_default_policy: str | None = None
    eip712_domain_allowlist: list[dict[str, Any]] | None = None
    api_key_prefix: str | None = None
    api_key_expires_at: str | None = None
    platform_app_id: str | None = None
    platform_locked: bool | None = None
    treasury_signing_mode: str | None = None


@dataclass
class AgentCreatedResponse:
    agent: AgentResponse
    api_key: str | None = None


@dataclass
class AgentListResponse:
    agents: list[AgentResponse] = field(default_factory=list)


@dataclass
class EnrollAgentRequest:
    name: str
    human_email: str
    description: str = ""


@dataclass
class EnrollAgentResponse:
    agent_id: str
    message: str


# ---------------------------------------------------------------------------
# Transactions / Intents API
# ---------------------------------------------------------------------------

@dataclass
class SubmitTransactionRequest:
    chain: str
    to: str
    value: str = "0"
    data: str | None = None
    nonce: int | None = None
    gas_limit: int | None = None
    gas_price: str | None = None
    max_fee_per_gas: str | None = None
    max_priority_fee_per_gas: str | None = None
    signing_key_path: str | None = None
    simulate_first: bool | None = None
    gasless: bool | None = None
    treasury_id: str | None = None
    mode: str | None = None
    destination_tag: int | None = None
    memo: str | None = None
    fee_rate_sat_per_vbyte: int | None = None
    fee_limit_sun: int | None = None
    token_mint: str | None = None
    token_decimals: int | None = None
    ttl: int | None = None
    xrpl_tx_json: dict[str, Any] | None = None


@dataclass
class TransactionResponse:
    id: str | None = None
    agent_id: str | None = None
    chain: str | None = None
    chain_id: int | None = None
    to_address: str | None = None
    value_wei: str | None = None
    data_hex: str | None = None
    signed_tx: str | None = None
    tx_hash: str | None = None
    from_address: str | None = None
    status: str | None = None
    nonce: int | None = None
    gas_limit: int | None = None
    created_at: str | None = None
    simulation_id: str | None = None
    simulation_status: str | None = None
    simulation_result: dict[str, Any] | None = None
    intent_type: str | None = None
    tx_type: int | None = None


@dataclass
class TransactionListResponse:
    transactions: list[TransactionResponse] = field(default_factory=list)


@dataclass
class SignIntentRequest:
    intent_type: str
    chain: str
    signing_key_path: str | None = None
    message: str | None = None
    typed_data: dict[str, Any] | None = None
    hash: str | None = None
    tx_type: int | None = None
    to: str | None = None
    value: str | None = None
    data: str | None = None
    nonce: int | None = None
    gas_limit: int | None = None
    gas_price: str | None = None
    max_fee_per_gas: str | None = None
    max_priority_fee_per_gas: str | None = None
    sign_only: bool | None = None
    destination_tag: int | None = None
    memo: str | None = None
    fee_rate_sat_per_vbyte: int | None = None
    fee_limit_sun: int | None = None
    token_mint: str | None = None
    token_decimals: int | None = None
    ttl: int | None = None
    xrpl_tx_json: dict[str, Any] | None = None


@dataclass
class SignIntentResponse:
    signature: str | None = None
    signed_tx: str | None = None
    tx_hash: str | None = None
    message_hash: str | None = None
    typed_data_hash: str | None = None
    from_address: str | None = None
    tx_type: int | None = None


# ---------------------------------------------------------------------------
# Signing Keys
# ---------------------------------------------------------------------------

@dataclass
class CreateSigningKeyRequest:
    chain: str


@dataclass
class SigningKeyResponse:
    agent_id: str
    chain: str
    curve: str | None = None
    public_key: str | None = None
    address: str | None = None
    is_active: bool | None = None
    created_at: str | None = None


@dataclass
class SigningKeyListResponse:
    signing_keys: list[SigningKeyResponse] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Chains
# ---------------------------------------------------------------------------

@dataclass
class ChainResponse:
    id: str
    name: str
    chain_id: int | None = None
    rpc_url: str | None = None
    explorer_url: str | None = None
    native_currency: str | None = None
    is_testnet: bool | None = None
    is_enabled: bool | None = None


@dataclass
class ChainListResponse:
    chains: list[ChainResponse] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Sharing
# ---------------------------------------------------------------------------

@dataclass
class CreateShareRequest:
    vault_id: str
    secret_path: str
    expires_in_hours: int = 24
    max_views: int | None = None
    passphrase: str | None = None
    recipient_type: str | None = None
    recipient_email: str | None = None
    ip_allowlist: list[str] | None = None


@dataclass
class ShareResponse:
    id: str
    share_url: str | None = None
    secret_path: str | None = None
    vault_id: str | None = None
    created_at: str | None = None
    expires_at: str | None = None
    max_views: int | None = None
    views: int | None = None
    status: str | None = None


@dataclass
class ShareListResponse:
    shares: list[ShareResponse] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Billing
# ---------------------------------------------------------------------------

@dataclass
class SubscriptionResponse:
    tier: str | None = None
    status: str | None = None
    period_end: str | None = None
    overage_method: str | None = None
    usage: dict[str, Any] | None = None


@dataclass
class CreditBalanceResponse:
    balance_cents: int | None = None
    expiring_soon: list[dict[str, Any]] | None = None


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

@dataclass
class AuditEventResponse:
    id: str
    action: str
    actor_id: str | None = None
    actor_type: str | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    timestamp: str | None = None
    ip_address: str | None = None
    details: dict[str, Any] | None = None


@dataclass
class AuditEventListResponse:
    events: list[AuditEventResponse] = field(default_factory=list)
    total: int | None = None


# ---------------------------------------------------------------------------
# Organization
# ---------------------------------------------------------------------------

@dataclass
class OrgMemberResponse:
    user_id: str
    email: str | None = None
    display_name: str | None = None
    role: str | None = None
    joined_at: str | None = None


@dataclass
class OrgMemberListResponse:
    members: list[OrgMemberResponse] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Treasury
# ---------------------------------------------------------------------------

@dataclass
class TreasuryResponse:
    id: str
    name: str
    org_id: str
    safe_address: str | None = None
    chain: str | None = None
    chain_id: int | None = None
    threshold: int | None = None
    created_at: str | None = None


@dataclass
class TreasuryListResponse:
    treasuries: list[TreasuryResponse] = field(default_factory=list)


@dataclass
class TreasuryWalletResponse:
    id: str
    chain: str
    address: str | None = None
    public_key_hex: str | None = None
    curve: str | None = None
    is_active: bool | None = None
    created_at: str | None = None


@dataclass
class TreasuryWalletListResponse:
    wallets: list[TreasuryWalletResponse] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Platform
# ---------------------------------------------------------------------------

@dataclass
class PlatformAppResponse:
    id: str
    name: str
    slug: str | None = None
    org_id: str | None = None
    description: str | None = None
    is_active: bool | None = None
    billing_model: str | None = None
    auth_mode: str | None = None
    created_at: str | None = None


@dataclass
class PlatformAppCreatedResponse:
    app: PlatformAppResponse
    api_key: str | None = None


@dataclass
class PlatformAppListResponse:
    apps: list[PlatformAppResponse] = field(default_factory=list)


@dataclass
class BootstrapResponse:
    claim_url: str | None = None
    claim_token: str | None = None
    connection_id: str | None = None
    summary: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Approvals
# ---------------------------------------------------------------------------

@dataclass
class ApprovalResponse:
    id: str
    action: str | None = None
    target_type: str | None = None
    target_id: str | None = None
    summary: str | None = None
    reason: str | None = None
    risk_tier: int | None = None
    status: str | None = None
    decided_by: str | None = None
    decided_at: str | None = None
    created_at: str | None = None


@dataclass
class ApprovalListResponse:
    approvals: list[ApprovalResponse] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Webhooks
# ---------------------------------------------------------------------------

@dataclass
class WebhookResponse:
    id: str
    url: str
    events: list[str] = field(default_factory=list)
    is_active: bool | None = None
    created_at: str | None = None


@dataclass
class WebhookListResponse:
    webhooks: list[WebhookResponse] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Risk Engine
# ---------------------------------------------------------------------------

@dataclass
class RiskEventResponse:
    id: str
    principal_type: str | None = None
    principal_id: str | None = None
    severity: str | None = None
    reasons: list[dict[str, Any]] | None = None
    ip_address: str | None = None
    created_at: str | None = None


@dataclass
class RiskVerdictResponse:
    principal_type: str
    principal_id: str
    severity: str | None = None
    reasons: list[dict[str, Any]] | None = None
    expires_at: str | None = None


@dataclass
class HoneytokenResponse:
    id: str
    vault_id: str | None = None
    secret_path: str | None = None
    trigger_count: int | None = None
    created_at: str | None = None


# ---------------------------------------------------------------------------
# API Keys
# ---------------------------------------------------------------------------

@dataclass
class CreateApiKeyRequest:
    name: str
    scopes: list[str] | None = None
    expires_at: str | None = None


@dataclass
class ApiKeyResponse:
    id: str
    name: str
    prefix: str | None = None
    scopes: list[str] | None = None
    created_at: str | None = None
    expires_at: str | None = None
    last_used_at: str | None = None


@dataclass
class ApiKeyCreatedResponse:
    key: ApiKeyResponse
    api_key: str


@dataclass
class ApiKeyListResponse:
    keys: list[ApiKeyResponse] = field(default_factory=list)
