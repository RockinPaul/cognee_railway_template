# Cognee Railway Deployment Template

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/cognee-ai-memory-p-1?referralCode=YqmMB-&utm_medium=integration&utm_source=template&utm_campaign=cognee)

Railway template for [cognee](https://github.com/topoteretes/cognee), the AI memory engine. It deploys:

- `cognee-api`: the cognee backend, from the upstream image `cognee/cognee:1.6.8`
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

**The MCP endpoint is public and unauthenticated by default** (single-user template,
`REQUIRE_AUTHENTICATION=false`). Anyone who reaches it can read and write your memory. URL secrecy
is not authentication: restrict MCP to a private network or put an authenticated gateway in front
before storing sensitive data.

**Backend authentication does not authenticate MCP callers.** With backend auth enabled, a
configured MCP backend credential is delegated to anonymous MCP callers too; this was verified by
an anonymous tool write/read against a private backend dataset. Keep that MCP endpoint private or
protect its transport separately. For an API key, use `COGNEE_API_KEY` and
`COGNEE_API_AUTH_SCHEME=x-api-key` on MCP; this keeps the key out of process arguments, unlike the
entrypoint's `API_TOKEN` CLI argument. If using JWTs, also set a stable random
`FASTAPI_USERS_JWT_SECRET` on the API so tokens remain valid across replacement.

## Variables you must provide

- `LLM_API_KEY`: an OpenRouter key for the LLM.
- `EMBEDDING_API_KEY`: defaults to `${{LLM_API_KEY}}` in the template. Override it only if embeddings use a different key. Do not leave it empty: with `LLM_PROVIDER=custom` cognee does not fall back to the LLM key, and ingestion fails with an embedding connection timeout.

Defaults: LLM `openrouter/openai/gpt-4o-mini`, embeddings `openrouter/openai/text-embedding-3-large` with 3072 dimensions. Single-user mode: `ENABLE_BACKEND_ACCESS_CONTROL=false`, `REQUIRE_AUTHENTICATION=false`.

**Cheaper LLM.** `LLM_MODEL=openrouter/deepseek/deepseek-v4-flash` was tested with this template and cuts output cost by about 70% versus `gpt-4o-mini`. Your notes are the payload sent to the model provider, so check the provider routing and data-retention policy in your OpenRouter account before switching a memory store to it.

Changing `EMBEDDING_MODEL` on a running deployment invalidates every stored vector. Pick it before adding data, or re-add everything after.

## How it fits together

- `cognee-mcp` reaches `cognee-api` over Railway private networking: `API_URL=http://cognee-api.railway.internal:8080`.
- Both services read every Postgres setting as `${{Postgres.*}}` references, so no credentials are typed in.
- `GRAPH_DATABASE_PROVIDER=postgres` keeps the whole stack on one database. Upstream labels this adapter demo-grade and recommends a graph-native store such as Neo4j for production workloads.
- There is no volume on `cognee-api`. Uploaded raw files live in the container and are lost on redeploy. Graph, vectors, and metadata persist in Postgres. If you add a volume at `/cognee-storage`, the image runs as uid 1000, so also set `RAILWAY_RUN_UID=0`.

## Upgrading cognee

Upgrade API and MCP together: API 1.6.8 and MCP `main-5870f15` were tested as a pair.
The MCP source declares 1.6.8 but comes from a different commit than the API release tag.

The standard template uses Postgres for relational/graph data and pgvector for vectors, with
3072-dimensional embeddings. **The Ladybug storage-format change is inapplicable to this layout**;
do not run a Ladybug/Kuzu migration against it. Check any custom backend override separately.

Before applying the pair, take a consistent Postgres backup and retain both old image identities.
For re-ingestion or full rollback, also copy `/cognee-storage` out of the old API container: there is
no API volume by default. Replacing the API loses raw uploaded/text files while Postgres graph,
vectors and metadata remain searchable. A database backup alone does not recover those raw files.

**Image-only downgrade is not supported.** The 1.6.6 API fails against the upgraded schema with
`Can't locate revision identified by 'e3f1a9c5b7d2'`. Rollback means restoring the untouched
pre-upgrade logical database backup, restoring the raw-file archive if needed, and running both
old images; do not run invented reverse SQL migrations. Coordinate writes while taking/restoring
the backup. The tested logical restore used `pg_restore --clean --if-exists` into a separate fresh
test database, never a live database. See [CHANGELOG.md](CHANGELOG.md) for the rehearsal boundary.

The populated Linux/amd64 rehearsal covered the actual Railway `postgres-ssl:18` source image,
old/new API-mode MCP writes/queries, exact data/vector/schema preservation, TLS 1.3 with SSL-mode
overrides unset, replacement, and logical backup/raw-file restoration with the old images.
The LLM/3072-dimensional embedding provider was a controlled local stub; no paid provider, live
production data or Railway deployment was tested.

### Ingestion choices

Leave `ALLOW_HTTP_REQUESTS` and `ALLOW_DATABASE_INGESTION` unset unless the operator deliberately
needs those sources. On `cognee-api`, unset/false refuses direct API URL/repository fetching and
database connection-string ingestion; local server file paths also require their separate opt-in.
Explicit `ALLOW_HTTP_REQUESTS=false` additionally disables outbound connector operations. Explicit
true does not bypass safety checks: private HTTP addresses and Cognee's own database server remain
refused. Model/embedding provider calls still use their configured endpoints.

For source ingestion, submit the HTTP API's explicit `raw_data` payload and set the relevant
opt-in on **the API service**, not only on MCP. API-mode MCP `remember(data=...)` in this pinned build
uploads non-file strings as literal text: URLs and DSNs are stored, not fetched. Enabling the API
opt-ins does not change that upload behavior. **Never hand a credential-bearing DSN to `remember`**;
it would become a document. SDK/direct-mode defaults are not evidence of API-mode behavior.

## Files

- `Dockerfile`: `cognee-api` image
- `Dockerfile.mcp`: `cognee-mcp` image, selected on that service by `RAILWAY_DOCKERFILE_PATH=Dockerfile.mcp`
- `railway.toml`: legacy Config-as-Code kept for pre-deprecation deployers until 2026-12-01
- `RAILWAY_SETUP.md`: how the Railway project and template are wired, for maintainers
- `TEMPLATE_OVERVIEW.md`: the marketplace description
- `CHANGELOG.md`: what changed and how to upgrade an existing deployment
