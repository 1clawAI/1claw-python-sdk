# 1Claw Python SDK

> ⭐ **Star [1clawAI/agent-templates](https://github.com/1clawAI/agent-templates)** — ready-to-run agent templates wired to 1Claw. It is our single starred repo.

Official Python client for the [1Claw](https://1claw.co) Vault API.

[![PyPI version](https://img.shields.io/pypi/v/oneclaw.svg)](https://pypi.org/project/oneclaw/)
[![Python versions](https://img.shields.io/pypi/pyversions/oneclaw.svg)](https://pypi.org/project/oneclaw/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Use this SDK when you're writing Python services, cron jobs, or agent backends that talk to 1Claw directly. It covers vaults, secrets, agents, policies, the Intents API, execution bindings, billing, and the rest of the REST surface.

Agent keys (`ocv_`) auto-exchange for short-lived JWTs and refresh before expiry. User keys (`1ck_`) work the same way. You do not need to hand-roll token rotation or parse error responses from scratch.

If you're using LangChain or CrewAI, consider [`langchain-1claw`](https://pypi.org/project/langchain-1claw/) or [`1claw-crewai-tools`](https://pypi.org/project/1claw-crewai-tools/) instead. They wrap this client as framework tools. This package is the low-level building block.

## Graduated HITL (v0.54–0.55)

Agent types include `tx_approval_policy`, `typed_data_policy`, `simulation_failure_policy`, `raw_signing_policy`, extended guardrails (`tx_block_unlimited_approvals`, USD caps, per-recipient limits), and `auto_suspended`. Matching transactions return **202** `awaiting_approval`; approve via `client.approvals.decide()`.

```python
await client.agents.update(agent_id, UpdateAgentRequest(
    tx_approval_policy={"require_above_native": {"ethereum": "0.1"}},
    typed_data_policy="approve",
    tx_block_unlimited_approvals=True,
))
```

## Installation

```bash
pip install oneclaw
```

## Quick Start

### Agent Authentication (API Key)

```python
from oneclaw import create_client

# Agent keys (ocv_) auto-exchange for JWTs and refresh before expiry
client = create_client(api_key="ocv_your_agent_key")

# Agent ID is auto-discovered from the token exchange
print(client.resolved_agent_id)
```

### User Authentication

```python
from oneclaw import create_client

# User API key (1ck_) — auto-exchanges for JWT
client = create_client(api_key="1ck_your_user_key")

# Or login with email/password
client = create_client()
client.auth.login("user@example.com", "password")
```

### Pre-authenticated with JWT

```python
client = create_client(token="eyJ...")
```

## Usage

### Vaults

```python
# Create a vault
resp = client.vaults.create("my-vault", description="Production secrets")
vault_id = resp.data["id"]

# List vaults
vaults = client.vaults.list()
for v in vaults.data["vaults"]:
    print(v["name"])
```

### Secrets

```python
# Store a secret
client.secrets.set(vault_id, "api-key", "sk-secret-value")

# Retrieve a secret
secret = client.secrets.get(vault_id, "api-key")
print(secret.data["value"])

# Server-side rotation (vault generates a random value)
client.secrets.rotate_generate(vault_id, "api-key", length=64, charset="base64")

# List versions
versions = client.secrets.list_versions(vault_id, "api-key")
```

### Agents

```python
# Register an agent
resp = client.agents.create("my-agent", description="CI/CD bot")
agent = resp.data["agent"]
api_key = resp.data["api_key"]  # Save this — shown only once

# Self-enroll (no auth required)
client.agents.enroll("my-agent", "admin@example.com")
```

### Agent Delegation

```python
# Create a delegation (human-only)
client.agents.create_delegation(
    orchestrator_id,
    delegate_id=sub_agent_id,
    allowed_tools=["delegate_task"],
    max_daily_delegations=100,
    delegation_mode="caller",
)

# List and query delegations
delegations = client.agents.list_delegations(agent_id)
effective = client.agents.get_effective_delegations(agent_id)

# Revoke a delegation
client.agents.revoke_delegation(agent_id, delegation_id)
```

### Access Policies

```python
# Grant an agent read access to secrets matching a pattern
client.policies.create(
    vault_id,
    principal_type="agent",
    principal_id=agent_id,
    secret_path_pattern="production/*",
    permissions=["read"],
)
```

### Intents API (Transaction Signing)

```python
# Submit a transaction
resp = client.agents.submit_transaction(
    agent_id,
    chain="ethereum",
    to="0x...",
    value="1000000000000000",  # wei
    max_fee_per_gas="30000000000",
    max_priority_fee_per_gas="1000000000",
)
print(resp.data["tx_hash"])

# Unified signing (personal_sign, typed_data, transaction)
resp = client.agents.sign_intent(
    agent_id,
    intent_type="personal_sign",
    chain="ethereum",
    message="0x48656c6c6f",
)
print(resp.data["signature"])

# Non-EVM: Solana devnet native transfer
resp = client.agents.submit_transaction(
    agent_id,
    chain="solana-devnet",
    to="RecipientBase58...",
    value="0.001",
)

# Non-EVM: Bitcoin testnet
resp = client.agents.sign_transaction(
    agent_id,
    chain="bitcoin-testnet",
    to="tb1q...",
    value="0.00001",
    fee_rate_sat_per_vbyte=5,
)
```

### Execution Intents (Bindings)

```python
# Create a binding with an inline credential
resp = client.bindings.create(
    agent_id,
    name="httpbin",
    binding_type="http",
    config={"base_url": "https://httpbin.org"},
    guardrails={"allowed_paths": ["/get", "/status/*"]},
    credential={"token": "secret"},
)
binding_id = resp.data["id"]

# Create a binding with a vault_ref credential (live-pointer to an existing secret)
resp = client.bindings.create(
    agent_id,
    name="stripe-api",
    binding_type="http",
    config={"base_url": "https://api.stripe.com"},
    credential_source={
        "type": "vault_ref",
        "vault_id": vault_id,
        "path": "integrations/stripe-key",
    },
)

# List bindings
bindings = client.bindings.list(agent_id)

# Test connectivity
result = client.bindings.test(agent_id, binding_id)

# Execute an HTTP intent
resp = client.bindings.execute(
    agent_id,
    binding="httpbin",
    intent_type="http",
    params={"method": "GET", "path": "/get"},
)
print(resp.data["execution_id"])

# Rotate credential (human-only)
client.bindings.rotate_credential(agent_id, binding_id, credential={"token": "new-secret"})

# List execution history
events = client.bindings.list_executions(agent_id, limit=20)

# Update guardrails
client.bindings.update(agent_id, binding_id, guardrails={"allowed_hosts": ["httpbin.org"]})

# Delete a binding
client.bindings.delete(agent_id, binding_id)
```

### Signing Keys

```python
# Provision a signing key
client.signing_keys.create(agent_id, "ethereum")

# List keys
keys = client.signing_keys.list(agent_id)

# Check balance
balance = client.signing_keys.balance(agent_id, "ethereum")
```

### Treasury

```python
# Create a treasury
client.treasury.create("Team Treasury", safe_address="0x...", chain="ethereum")

# Create a multisig proposal
client.treasury.propose(treasury_id, chain="ethereum", to="0x...", value="1000000000")

# Sign a proposal
client.treasury.sign_proposal(treasury_id, proposal_id, signature="0x...", decision="approve")
```

### Treasury Wallets

```python
# Generate wallets for all supported chains
client.treasury_wallets.generate()

# Check balance
balance = client.treasury_wallets.balance("ethereum")

# Send tokens (requires password re-auth)
client.treasury_wallets.send(
    "ethereum",
    to="0x...",
    value="1000000000000000",
    password="your-account-password",
)
```

### Platform API

```python
# Register a platform app
resp = client.platform.create_app("My App", "my-app")
plt_key = resp.data["api_key"]  # Save this

# Provision a user
conn = client.platform.upsert_user(email="user@example.com")

# Bootstrap resources from a template
bootstrap = client.platform.bootstrap_user(conn.data["connection_id"])

# Browse the public marketplace (no auth required)
apps = client.platform.marketplace(category="finance")

# Get app stats (connections, bootstraps, grants)
stats = client.platform.get_app_stats(app_id)

# Rotate webhook signing secret (returns new secret once)
secret = client.platform.rotate_webhook_secret(app_id)
```

### Webhooks

```python
client.webhooks.create(
    url="https://example.com/webhook",
    events=["agent.transaction.broadcast", "proposal.executed"],
    secret="whsec_...",
)
```

### Risk Engine

```python
# List risk events
events = client.risk.list_events(severity="high")

# Register a honeytoken
client.risk.create_honeytoken(vault_id, "canary/secret-key")
```

### DPoP (Proof-of-Possession)

```python
client = create_client(api_key="ocv_...", dpop=True)
```

### Approvals

```python
approvals = client.approvals.list(status="pending")
client.approvals.decide(approval_id, "approved")
```

### Email OTP & OAuth

```python
client.auth.send_email_otp("user@example.com")
resp = client.auth.verify_email_otp("user@example.com", "123456")

client.auth.social_login(provider="google", id_token="...")

# Revoke an OAuth token (RFC 7009)
client.oauth_connect.revoke_token("eyJ...", token_type_hint="access_token")

# Revoke consent for a platform app (deletes consent + revokes all tokens)
client.oauth_connect.revoke_consent(app_id)
```

> **Note:** For the full API surface (non-EVM transaction signing, spend policies, deposit destinations, fiat ramps, internal accounts, and more), see the [TypeScript SDK](https://www.npmjs.com/package/@1claw/sdk) and the [OpenAPI spec](https://www.npmjs.com/package/@1claw/openapi-spec).

### Automations

```python
# Create a cron-based automation (workflow_spec required)
client.automations.create(
    name="rotate-api-key",
    agent_id=agent_id,
    trigger_type="cron",
    cron_expr="0 0 * * 0",  # weekly
    timezone="UTC",
    workflow_spec={
        "steps": [
            {"type": "log", "action": "run_agent_task", "message": "Rotate weekly API keys"}
        ]
    },
)

# List automations in the org
autos = client.automations.list()

# Manually trigger
client.automations.trigger(automation_id)

# Get a specific run
run = client.automations.get_run(automation_id, run_id)

# Cancel a running automation (human-only)
client.automations.cancel_run(automation_id, run_id)

# Browse preset templates (public, no auth)
presets = client.automations.list_presets()
```

### Channels

```python
# Register a Telegram channel for an agent (human-only)
ch = client.channels.create(agent_id, "telegram", channel_name="Support Bot")

# List channels
channels = client.channels.list(agent_id)

# Send a message via a channel
client.channels.send_message(agent_id, channel_id, content="Hello from 1Claw!")

# List message history
messages = client.channels.list_messages(agent_id, channel_id)
```

### Agent Memory

```python
# Store a memory entry (namespace + key)
client.memory.put(agent_id, "preferences", "output_format", value="JSON")

# Get a specific entry
entry = client.memory.get(agent_id, "preferences", "output_format")

# Semantic search within a namespace
results = client.memory.search(agent_id, namespace="preferences", query="output format", top_k=5)

# List entries in a namespace
entries = client.memory.list(agent_id, "preferences")

# List all namespaces
namespaces = client.memory.list_namespaces(agent_id)

# Delete an entry
client.memory.delete(agent_id, "preferences", "output_format")

# Delete an entire namespace
client.memory.delete_namespace(agent_id, "preferences")
```

### Runtimes

```python
# Deploy a runtime
runtime = client.runtimes.create(
    agent_id=agent_id,
    name="my-agent-runtime",
    template="python",
    preset="small",
    env_public={"MODEL": "gpt-4"},
    shell_access_enabled=True,
)

# List runtimes
runtimes = client.runtimes.list()

# Lifecycle
client.runtimes.start(runtime_id)
logs = client.runtimes.logs(runtime_id, limit=100)
client.runtimes.stop(runtime_id)

# Interactive shell (human-only, step-up password / passkey / reauth token)
session = client.runtimes.create_shell_session(runtime_id, password="...")
# Connect a WebSocket client to session.data["ws_url"] with the session_token
```

### Discovery

```python
# Publish agent to directory
client.discovery.publish(
    agent_id,
    description="Automated treasury management agent",
    tags=["defi", "treasury", "base"],
    category="finance",
)

# Search the directory
results = client.discovery.search(query="treasury management", tags=["defi"])

# Update listing
client.discovery.update_listing(agent_id, tags=["defi", "treasury", "ethereum", "base"])
```

## Error Handling

```python
from oneclaw import create_client, OneclawError, AuthError, NotFoundError

client = create_client(api_key="ocv_...")

# Envelope-style (no exceptions)
resp = client.vaults.get("nonexistent-id")
if resp.error:
    print(f"Error: {resp.error.message}")

# Exception-style (use the underlying HTTP client)
try:
    data = client._http.request_or_throw("GET", "/v1/vaults/bad-id")
except NotFoundError:
    print("Vault not found")
except AuthError:
    print("Authentication failed")
except OneclawError as e:
    print(f"API error: {e} (status={e.status})")
```

## Context Manager

```python
with create_client(api_key="ocv_...") as client:
    vaults = client.vaults.list()
    # Connection pool is automatically closed
```

## v0.56 — Safe accounts, guardrail governance, HFA

```python
# Agent on-chain accounts (EOA + counterfactual Safe)
accounts = client.agents.list_accounts(agent_id)
plan = client.agents.migrate_to_safe(agent_id, chain="ethereum", deprecate_eoa=True)
client.agents.deprecate_eoa_account(agent_id, "ethereum")
registry = client.agents.get_safe_module_registry("ethereum")  # public
client.agents.sync_org_safe_allowances()  # owner/admin

# Guardrail governance
client.org.get_guardrail_shadow_report(since="2026-01-01T00:00:00Z")
client.org.list_guardrail_revisions()
client.agents.replay_guardrails(agent_id, draft_guardrails={"tx_max_value_eth": "0.1"})

# Human Factor Auth
client.auth.get_human_factor_auth()
client.auth.set_human_factor_auth({"require_passkey": True})
client.treasury_wallets.get_auth_policy()  # embedded wallet clients
```

## v0.57 — Platform API expansion

```python
challenge = client.platform.siwe_challenge()
conn = client.platform.get_connection(connection_id)
usage = client.platform.get_connection_usage(connection_id)
entitlements = client.platform.list_entitlements(connection_id)
preview = client.platform.preview_template(app_id, template_id, parameters={"agent_name": "demo"})
```

## v0.58 — Platform control plane

```python
client.platform.transfer_app_ownership(app_id, target_org_id="...")
client.platform.get_spend_policy(app_id, policy_id)
client.platform.get_connection_spend_policy(connection_id)
client.platform.list_connection_approvals(connection_id)
client.platform.get_connection_approval(connection_id, approval_id)
client.platform.list_connection_pending_approvals(connection_id)
```

## v0.59 — Platform connection expansion

```python
# Signing keys + agent patch (plt_ auth — not org-scoped /agents routes)
client.platform.list_connection_signing_keys(connection_id, agent_id=agent_id)
client.platform.get_connection_signing_key(connection_id, "ethereum", agent_id=agent_id)
client.platform.patch_connection_agent(connection_id, agent_id, {
    "intents_api_enabled": True,
    "system_prompt": "You are a DeFi bot.",
})

# Portfolio, pending-approval create, automations, memory (v0.59.9)
portfolio = client.platform.get_connection_portfolio(connection_id, include_tokens=True)
pending = client.platform.create_connection_pending_approval(connection_id, {
    "agent_id": agent_id,
    "action": "transaction",
    "action_payload": {"chain": "ethereum", "to": "0x...", "value": "0.1"},
})
autos = client.platform.list_connection_automations(connection_id)
client.platform.put_connection_memory(connection_id, "default", "pref", {"value": "..."}, agent_id=agent_id)
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `base_url` | `https://api.1claw.co` | API base URL |
| `token` | `None` | Pre-existing JWT |
| `api_key` | `None` | `ocv_` (agent) or `1ck_` (user) key |
| `agent_id` | `None` | Agent UUID (optional, auto-discovered) |
| `timeout` | `30.0` | HTTP timeout in seconds |

## Requirements

- Python 3.9+
- [httpx](https://www.python-httpx.org/) (only runtime dependency)

## License

MIT
