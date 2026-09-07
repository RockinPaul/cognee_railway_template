# Cognee Railway Deployment Template

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/cognee-ai-memory-p-1?referralCode=YqmMB-&utm_medium=integration&utm_source=template&utm_campaign=cognee)

Railway template for [cognee](https://github.com/topoteretes/cognee), the AI memory engine. It deploys:

- `cognee-api`: the cognee backend, from the upstream image `cognee/cognee:1.5.4`
- `cognee-mcp`: the cognee MCP server in API mode, exposed publicly with Streamable HTTP at `/mcp`
- `Postgres`: one managed Postgres with pgvector for relational, graph, and vector storage

This repo holds only what Railway needs: two one-line Dockerfiles over the upstream images plus docs. Cognee itself is not vendored here.

## Connect an MCP client

After deploy, open the `cognee-mcp` service, copy its public domain, and point your client at `/mcp`.

OpenCode:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "cognee": {
      "type": "remote",
      "url": "https://<cognee-mcp-domain>.up.railway.app/mcp",
      "enabled": true
    }
  }
}
```

Claude Code:

```bash
claude mcp add --transport http cognee https://<cognee-mcp-domain>.up.railway.app/mcp
```

Prefer the legacy SSE transport? Set `TRANSPORT_MODE=sse` on `cognee-mcp` and use `/sse` instead.

**The MCP endpoint is public and unauthenticated by design** (single-user template, `REQUIRE_AUTHENTICATION=false`). Anyone who learns the URL can read and write your memory. Treat the domain like a secret, or turn on backend authentication and set `API_TOKEN` on `cognee-mcp`.

## Variables you must provide

- `LLM_API_KEY`: an OpenRouter key for the LLM.
- `EMBEDDING_API_KEY`: defaults to `${{LLM_API_KEY}}` in the template. Override it only if embeddings use a different key. Do not leave it empty: with `LLM_PROVIDER=custom` cognee does not fall back to the LLM key, and ingestion fails with an embedding connection timeout.

Defaults: LLM `openrouter/openai/gpt-4o-mini`, embeddings `openrouter/google/gemini-embedding-2-preview` with 3072 dimensions. Single-user mode: `ENABLE_BACKEND_ACCESS_CONTROL=false`, `REQUIRE_AUTHENTICATION=false`.

## How it fits together

- `cognee-mcp` reaches `cognee-api` over Railway private networking: `API_URL=http://cognee-api.railway.internal:8080`.
- Both services read every Postgres setting as `${{Postgres.*}}` references, so no credentials are typed in.
- `GRAPH_DATABASE_PROVIDER=postgres` keeps the whole stack on one database. Upstream labels this adapter demo-grade and recommends a graph-native store such as Neo4j for production workloads.
- There is no volume on `cognee-api`. Uploaded raw files live in the container and are lost on redeploy. Graph, vectors, and metadata persist in Postgres. If you add a volume at `/cognee-storage`, the image runs as uid 1000, so also set `RAILWAY_RUN_UID=0`.

## Upgrading cognee

Bump the tag in `Dockerfile` (`cognee/cognee:<version>`) and, when upstream publishes a matching build, in `Dockerfile.mcp`. Merging to `main` notifies everyone who deployed the template. Record breaking changes in `CHANGELOG.md`.

## Files

- `Dockerfile`: `cognee-api` image
- `Dockerfile.mcp`: `cognee-mcp` image, selected on that service by `RAILWAY_DOCKERFILE_PATH=Dockerfile.mcp`
- `railway.toml`: legacy Config-as-Code kept for pre-deprecation deployers until 2026-12-01
- `RAILWAY_SETUP.md`: how the Railway project and template are wired, for maintainers
- `TEMPLATE_OVERVIEW.md`: the marketplace description
- `CHANGELOG.md`: what changed and how to upgrade an existing deployment
