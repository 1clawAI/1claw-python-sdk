"""Environment variables resource."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from oneclaw.http_client import HttpClient
    from oneclaw.types import OneclawResponse


class EnvVarsResource:
    """Environment variable CRUD within a vault — create, list, resolve, update, delete."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(
        self,
        vault_id: str,
        *,
        environment: str | None = None,
    ) -> OneclawResponse[Any]:
        """List environment variables in a vault, optionally filtered by environment."""
        query: dict[str, str] = {}
        if environment is not None:
            query["environment"] = environment
        return self._http.request(
            "GET", f"/v1/vaults/{vault_id}/env-vars", query=query or None,
        )

    def create(
        self,
        vault_id: str,
        key: str,
        value: str,
        *,
        environments: List[str] | None = None,
        git_branch: str | None = None,
        sensitive: bool = False,
        comment: str | None = None,
    ) -> OneclawResponse[Any]:
        """Create an environment variable in a vault."""
        body: dict[str, Any] = {"key": key, "value": value, "sensitive": sensitive}
        if environments is not None:
            body["environments"] = environments
        if git_branch is not None:
            body["git_branch"] = git_branch
        if comment is not None:
            body["comment"] = comment
        return self._http.request("POST", f"/v1/vaults/{vault_id}/env-vars", body=body)

    def get(
        self,
        vault_id: str,
        key: str,
        *,
        environment: str | None = None,
        git_branch: str | None = None,
    ) -> OneclawResponse[Any]:
        """Retrieve a single environment variable by key."""
        query: dict[str, str] = {}
        if environment is not None:
            query["environment"] = environment
        if git_branch is not None:
            query["git_branch"] = git_branch
        return self._http.request(
            "GET", f"/v1/vaults/{vault_id}/env-vars/{key}", query=query or None,
        )

    def update(
        self,
        vault_id: str,
        key: str,
        *,
        value: str | None = None,
        environments: List[str] | None = None,
        sensitive: bool | None = None,
        comment: str | None = None,
        environment: str | None = None,
        git_branch: str | None = None,
    ) -> OneclawResponse[Any]:
        """Update an environment variable."""
        body: dict[str, Any] = {}
        if value is not None:
            body["value"] = value
        if environments is not None:
            body["environments"] = environments
        if sensitive is not None:
            body["sensitive"] = sensitive
        if comment is not None:
            body["comment"] = comment
        query: dict[str, str] = {}
        if environment is not None:
            query["environment"] = environment
        if git_branch is not None:
            query["git_branch"] = git_branch
        return self._http.request(
            "PATCH", f"/v1/vaults/{vault_id}/env-vars/{key}",
            body=body,
            query=query or None,
        )

    def delete(
        self,
        vault_id: str,
        key: str,
        *,
        environment: str | None = None,
        git_branch: str | None = None,
    ) -> OneclawResponse[Any]:
        """Delete an environment variable."""
        query: dict[str, str] = {}
        if environment is not None:
            query["environment"] = environment
        if git_branch is not None:
            query["git_branch"] = git_branch
        return self._http.request(
            "DELETE", f"/v1/vaults/{vault_id}/env-vars/{key}", query=query or None,
        )

    def resolve(
        self,
        vault_id: str,
        environment: str,
        *,
        git_branch: str | None = None,
    ) -> OneclawResponse[Any]:
        """Resolve all environment variables for a given environment.

        Returns a merged key-value map with source attribution (shared, vault,
        or branch override).
        """
        query: dict[str, str] = {"environment": environment}
        if git_branch is not None:
            query["git_branch"] = git_branch
        return self._http.request(
            "GET", f"/v1/vaults/{vault_id}/env-vars/resolve", query=query,
        )

    # ── Vault environments ──────────────────────────────────

    def list_environments(self, vault_id: str) -> OneclawResponse[Any]:
        """List available environments for a vault."""
        return self._http.request("GET", f"/v1/vaults/{vault_id}/environments")

    def create_environment(
        self,
        vault_id: str,
        slug: str,
        *,
        description: str | None = None,
        copy_from: str | None = None,
    ) -> OneclawResponse[Any]:
        """Create a custom environment for a vault."""
        body: dict[str, Any] = {"slug": slug}
        if description is not None:
            body["description"] = description
        if copy_from is not None:
            body["copy_from"] = copy_from
        return self._http.request(
            "POST", f"/v1/vaults/{vault_id}/environments", body=body,
        )

    def delete_environment(self, vault_id: str, slug: str) -> OneclawResponse[Any]:
        """Delete a custom environment from a vault."""
        return self._http.request(
            "DELETE", f"/v1/vaults/{vault_id}/environments/{slug}",
        )
