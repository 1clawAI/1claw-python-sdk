"""Tests for the OneclawClient."""


import httpx
import pytest
import respx

from oneclaw import OneclawError, create_client

BASE = "https://api.1claw.co"


@respx.mock
def test_create_client_with_token():
    client = create_client(token="eyJ.test.token")
    assert client._http.get_token() == "eyJ.test.token"


@respx.mock
def test_list_vaults():
    respx.get(f"{BASE}/v1/vaults").mock(
        return_value=httpx.Response(
            200, json={"vaults": [{"id": "v1", "name": "test", "org_id": "o1"}]},
        )
    )
    client = create_client(token="tok")
    resp = client.vaults.list()
    assert resp.error is None
    assert len(resp.data["vaults"]) == 1
    assert resp.data["vaults"][0]["name"] == "test"


@respx.mock
def test_create_vault():
    respx.post(f"{BASE}/v1/vaults").mock(
        return_value=httpx.Response(200, json={"id": "v1", "name": "new-vault", "org_id": "o1"})
    )
    client = create_client(token="tok")
    resp = client.vaults.create("new-vault", description="A vault")
    assert resp.data["name"] == "new-vault"


@respx.mock
def test_get_secret():
    respx.get(f"{BASE}/v1/vaults/v1/secrets/my-key").mock(
        return_value=httpx.Response(
            200, json={"path": "my-key", "value": "secret123", "version": 1},
        )
    )
    client = create_client(token="tok")
    resp = client.secrets.get("v1", "my-key")
    assert resp.data["value"] == "secret123"


@respx.mock
def test_put_secret():
    respx.put(f"{BASE}/v1/vaults/v1/secrets/my-key").mock(
        return_value=httpx.Response(200, json={"path": "my-key", "version": 2})
    )
    client = create_client(token="tok")
    resp = client.secrets.set("v1", "my-key", "new-value", type="api_key")
    assert resp.data["version"] == 2


@respx.mock
def test_error_handling_404():
    respx.get(f"{BASE}/v1/vaults/bad-id").mock(
        return_value=httpx.Response(404, json={"detail": "Vault not found"})
    )
    client = create_client(token="tok")
    resp = client.vaults.get("bad-id")
    assert resp.error is not None
    assert resp.error.type == "not_found"
    assert resp.meta.status == 404


@respx.mock
def test_error_handling_401():
    respx.get(f"{BASE}/v1/vaults").mock(
        return_value=httpx.Response(401, json={"detail": "Invalid token"})
    )
    client = create_client(token="bad-tok")
    resp = client.vaults.list()
    assert resp.error is not None
    assert resp.error.type == "auth_error"


@respx.mock
def test_request_or_throw():
    respx.get(f"{BASE}/v1/vaults/bad-id").mock(
        return_value=httpx.Response(404, json={"detail": "Not found"})
    )
    client = create_client(token="tok")
    with pytest.raises(OneclawError) as exc_info:
        client._http.request_or_throw("GET", "/v1/vaults/bad-id")
    assert exc_info.value.status == 404


@respx.mock
def test_create_agent():
    respx.post(f"{BASE}/v1/agents").mock(
        return_value=httpx.Response(200, json={
            "agent": {"id": "a1", "name": "bot", "org_id": "o1"},
            "api_key": "ocv_test",
        })
    )
    client = create_client(token="tok")
    resp = client.agents.create("bot", intents_api_enabled=True)
    assert resp.data["agent"]["name"] == "bot"
    assert resp.data["api_key"] == "ocv_test"


@respx.mock
def test_list_chains():
    respx.get(f"{BASE}/v1/chains").mock(
        return_value=httpx.Response(200, json={"chains": [
            {"id": "1", "name": "ethereum", "chain_id": 1},
        ]})
    )
    client = create_client(token="tok")
    resp = client.chains.list()
    assert resp.data["chains"][0]["name"] == "ethereum"


@respx.mock
def test_create_policy():
    respx.post(f"{BASE}/v1/vaults/v1/policies").mock(
        return_value=httpx.Response(200, json={
            "id": "p1", "vault_id": "v1",
            "principal_type": "agent", "principal_id": "a1",
            "secret_path_pattern": "prod/*", "permissions": ["read"],
        })
    )
    client = create_client(token="tok")
    resp = client.policies.create(
        "v1", principal_type="agent", principal_id="a1",
        secret_path_pattern="prod/*",
    )
    assert resp.data["permissions"] == ["read"]


@respx.mock
def test_agent_token_auto_refresh():
    respx.post(f"{BASE}/v1/auth/agent-token").mock(
        return_value=httpx.Response(200, json={
            "access_token": "jwt.payload.sig",
            "expires_in": 3600,
            "agent_id": "a1",
            "vault_ids": ["v1"],
        })
    )
    respx.get(f"{BASE}/v1/vaults").mock(
        return_value=httpx.Response(200, json={"vaults": []})
    )
    client = create_client(api_key="ocv_testkey", agent_id="a1")
    resp = client.vaults.list()
    assert resp.error is None
    assert client.resolved_agent_id == "a1"


@respx.mock
def test_204_response():
    respx.delete(f"{BASE}/v1/vaults/v1").mock(
        return_value=httpx.Response(204)
    )
    client = create_client(token="tok")
    resp = client.vaults.delete("v1")
    assert resp.error is None
    assert resp.meta.status == 204


@respx.mock
def test_context_manager():
    with create_client(token="tok") as client:
        assert client._http.get_token() == "tok"


@respx.mock
def test_submit_transaction():
    respx.post(f"{BASE}/v1/agents/a1/transactions").mock(
        return_value=httpx.Response(200, json={
            "id": "tx1", "status": "broadcast", "tx_hash": "0xabc",
        })
    )
    client = create_client(token="tok")
    resp = client.agents.submit_transaction(
        "a1", chain="ethereum", to="0x1234", value="1000000",
    )
    assert resp.data["tx_hash"] == "0xabc"


@respx.mock
def test_signing_keys_create():
    respx.post(f"{BASE}/v1/agents/a1/signing-keys").mock(
        return_value=httpx.Response(200, json={
            "agent_id": "a1", "chain": "ethereum", "address": "0xabc",
        })
    )
    client = create_client(token="tok")
    resp = client.signing_keys.create("a1", "ethereum")
    assert resp.data["chain"] == "ethereum"


@respx.mock
def test_webhook_create():
    respx.post(f"{BASE}/v1/webhooks").mock(
        return_value=httpx.Response(200, json={
            "id": "w1", "url": "https://example.com/hook",
            "events": ["agent.transaction.broadcast"],
        })
    )
    client = create_client(token="tok")
    resp = client.webhooks.create(
        url="https://example.com/hook",
        events=["agent.transaction.broadcast"],
    )
    assert resp.data["url"] == "https://example.com/hook"


@respx.mock
def test_audit_list_uses_events_route():
    route = respx.get(f"{BASE}/v1/audit/events").mock(
        return_value=httpx.Response(200, json={"events": [], "count": 0})
    )
    client = create_client(token="tok")
    resp = client.audit.list(action="secret.read", from_time="2026-10-01T00:00:00Z", limit=5)
    assert resp.error is None
    params = route.calls.last.request.url.params
    assert params["action"] == "secret.read"
    assert params["from"] == "2026-10-01T00:00:00Z"
    assert params["limit"] == "5"


@respx.mock
def test_sharing_routes_match_the_api():
    create = respx.post(f"{BASE}/v1/secrets/s1/share").mock(
        return_value=httpx.Response(201, json={"id": "sh1", "share_url": "u"})
    )
    outbound = respx.get(f"{BASE}/v1/shares/outbound").mock(
        return_value=httpx.Response(200, json={"shares": []})
    )
    revoke = respx.delete(f"{BASE}/v1/share/sh1").mock(return_value=httpx.Response(204))
    access = respx.get(f"{BASE}/v1/share/sh1").mock(
        return_value=httpx.Response(200, json={"value": "x"})
    )
    client = create_client(token="tok")
    resp = client.sharing.create(
        "s1",
        recipient_type="anyone_with_link",
        expires_at="2026-11-01T00:00:00Z",
        max_access_count=3,
    )
    assert resp.error is None
    import json as _json

    body = _json.loads(create.calls.last.request.content)
    assert body == {
        "recipient_type": "anyone_with_link",
        "expires_at": "2026-11-01T00:00:00Z",
        "max_access_count": 3,
    }
    assert client.sharing.list_outbound().error is None
    assert client.sharing.revoke("sh1").meta.status == 204
    assert client.sharing.access("sh1", passphrase="pw").data == {"value": "x"}
    assert _json.loads(access.calls.last.request.content) == {"passphrase": "pw"}
    assert outbound.called and revoke.called


@respx.mock
def test_org_update_setting_patches_collection():
    route = respx.patch(f"{BASE}/v1/org/settings").mock(
        return_value=httpx.Response(200, json={"key": "k", "value": "v"})
    )
    client = create_client(token="tok")
    assert client.org.update_setting("k", "v").error is None
    import json as _json

    assert _json.loads(route.calls.last.request.content) == {"key": "k", "value": "v"}


@respx.mock
def test_channels_get_filters_the_list():
    respx.get(f"{BASE}/v1/agents/a1/channels").mock(
        return_value=httpx.Response(200, json={"channels": [{"id": "c1"}, {"id": "c2"}]})
    )
    client = create_client(token="tok")
    assert client.channels.get("a1", "c2").data == {"id": "c2"}
    missing = client.channels.get("a1", "c9")
    assert missing.error is not None and missing.meta.status == 404
