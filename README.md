# 1Claw Python SDK

Official Python SDK for the [1Claw](https://1claw.xyz) secrets management platform.

[![PyPI version](https://img.shields.io/pypi/v/oneclaw.svg)](https://pypi.org/project/oneclaw/)
[![Python versions](https://img.shields.io/pypi/pyversions/oneclaw.svg)](https://pypi.org/project/oneclaw/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
```

> **Note:** For the full API surface (non-EVM transaction signing, spend policies, deposit destinations, fiat ramps, internal accounts, and more), see the [TypeScript SDK](https://www.npmjs.com/package/@1claw/sdk) and the [OpenAPI spec](https://www.npmjs.com/package/@1claw/openapi-spec).

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

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `base_url` | `https://api.1claw.xyz` | API base URL |
| `token` | `None` | Pre-existing JWT |
| `api_key` | `None` | `ocv_` (agent) or `1ck_` (user) key |
| `agent_id` | `None` | Agent UUID (optional, auto-discovered) |
| `timeout` | `30.0` | HTTP timeout in seconds |

## Requirements

- Python 3.9+
- [httpx](https://www.python-httpx.org/) (only runtime dependency)

## License

MIT
