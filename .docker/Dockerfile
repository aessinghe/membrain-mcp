ARG PYTHON_VERSION="3.12"

ARG BUILDER_IMAGE="public.ecr.aws/docker/library/python:${PYTHON_VERSION}-slim"
ARG RUNNER_IMAGE="public.ecr.aws/docker/library/python:${PYTHON_VERSION}-slim"

FROM ${BUILDER_IMAGE} AS builder
# Official, static uv binary - see https://docs.astral.sh/uv/guides/integration/docker/
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv
WORKDIR /app
# Install dependencies before copying the source so this (slow) layer is cached
# across source-only changes. --frozen refuses to touch uv.lock (it must already be
# up to date and committed); dev dependencies are an opt-in extra, so a plain
# `uv sync` here already excludes them.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
# README.md is required here too: hatchling reads pyproject.toml's `readme` field
# and refuses to build the project's own metadata if the file is missing.
COPY src/ ./src/
COPY README.md ./
RUN uv sync --frozen

FROM ${RUNNER_IMAGE}
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends --assume-yes \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
ADD ./.docker/entrypoint.sh /home/user/app/entrypoint.sh
RUN chmod 755 /home/user/app/entrypoint.sh \
    && useradd -d /home/user -s /bin/bash user
WORKDIR /home/user/app
COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src
ENV PATH="/home/user/app/.venv/bin:${PATH}" \
    MCP_TRANSPORT=http \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=8080 \
    PYTHONUNBUFFERED=1 \
    # FastMCP otherwise pings pypi.org at every startup to check for a newer
    # version - unwanted egress in a locked-down cluster network, and pointless
    # noise in container logs. Also drop its ASCII banner from stdout.
    FASTMCP_CHECK_FOR_UPDATES=off \
    FASTMCP_SHOW_SERVER_BANNER=false
USER user
EXPOSE 8080
ENTRYPOINT ["/home/user/app/entrypoint.sh"]
