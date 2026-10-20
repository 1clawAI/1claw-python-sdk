# Changelog

## 0.61.14

Route fixes. Each of these called a path the API does not serve and got a 404.

- `audit.list` calls `GET /v1/audit/events` (was `/v1/audit`). Adds `from_time` / `to_time`.
  `resource_type` is still accepted but not sent; the API has no such filter.
- `sharing`:
  - `create(secret_id, *, recipient_type, expires_at, ...)` posts to
    `/v1/secrets/{secret_id}/share` with the body the API expects (`recipient_type`,
    `expires_at`, optional `recipient_id`, `email`, `permissions`, `max_access_count`,
    `passphrase`, `ip_allowlist`). The old `vault_id` / `secret_path` / `expires_in_hours`
    arguments are gone; that call never worked.
  - `list_outbound` calls `/v1/shares/outbound`.
  - `revoke` (and its alias `delete`) calls `DELETE /v1/share/{share_id}`.
  - `access` calls `GET /v1/share/{share_id}`, passphrase in the body, and sends the
    client's token when it has one (needed for user/agent-targeted shares).
  - `get` removed: the API has no single-share read for the creator.
- `org.update_setting` sends `PATCH /v1/org/settings` with `{key, value}` (was
  `PUT /v1/org/settings/{key}`). Optional `approval_id`.
- `channels.get` lists the agent's channels and returns the matching one; the API has no
  single-channel GET.
