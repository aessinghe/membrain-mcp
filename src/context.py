"""Application context shared across tool calls via the FastMCP lifespan."""

from __future__ import annotations

from dataclasses import dataclass

from src.membrain_client import MembrainClient


@dataclass
class AppContext:
    """Holds the single, long-lived MembrainClient instance for the server's lifetime."""

    client: MembrainClient
