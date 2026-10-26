"""Runtime configuration for the Membrain MCP server, loaded from environment variables."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven settings. See .env.example for the full list of variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    membrain_base_url: str = Field(
        default="https://<your-domain>.membrain.com/API/v2/",
        description="Entry point of the Membrain REST API v2 for this tenant.",
    )
    membrain_api_key: SecretStr = Field(
        description="Membrain API key used to authenticate every request.",
    )
    membrain_timeout_seconds: float = Field(
        default=30.0,
        gt=0,
        description="Per-request HTTP timeout in seconds.",
    )
    membrain_max_retries: int = Field(
        default=3,
        ge=0,
        description="Max retry attempts for idempotent requests on transient errors.",
    )

    # Server-runtime settings (not Membrain API settings): how this MCP server itself
    # is exposed. Defaults preserve today's local stdio usage (Claude Desktop/Code
    # spawning the process directly via `uv run`); the containerized/EKS deployment
    # overrides these via env vars to run in HTTP mode instead (see .docker/Dockerfile).
    mcp_transport: Literal["stdio", "http"] = Field(
        default="stdio",
        description="'stdio' for local use (spawned by Claude Desktop/Code); 'http' "
        "for a remote/containerized deployment (e.g. EKS).",
    )
    mcp_host: str = Field(
        # Intentional: the container/pod must accept traffic from outside its own
        # network namespace (from the Service/ingress), not just from localhost.
        default="0.0.0.0",  # nosec B104
        description="Bind address used when mcp_transport is 'http'.",
    )
    mcp_port: int = Field(
        default=8080,
        gt=0,
        lt=65536,
        description="Bind port used when mcp_transport is 'http'.",
    )
