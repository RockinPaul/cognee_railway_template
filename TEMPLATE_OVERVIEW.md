# Deploy and Host Cognee AI Memory Platform with MCP on Railway

Cognee AI Memory Platform with MCP combines a Cognee backend, durable Postgres + pgvector storage,
and an MCP service so AI tools can store, structure, and retrieve memory across sessions. The template
runs API 1.6.8 with MCP `main-5870f15`, OpenRouter-backed models and Streamable HTTP. Its default
single-user MCP endpoint is public and unauthenticated: anyone who reaches it can read/write memory.
Keep MCP private or protect it with an authenticated gateway before storing sensitive content.
Backend API authentication and an MCP backend key do not authenticate MCP callers.

## About Hosting Cognee AI Memory Platform with MCP

Hosting this template deploys three connected services: `cognee-api` as the backend, `cognee-mcp`
as the MCP layer, and PostgreSQL as the shared relational, graph, and vector store. The MCP service
reaches the backend over private networking. Public exposure still needs the access boundary
described above. The single-user stack supports ingestion, Cognify, search and MCP access; supply
an OpenRouter API key, which embeddings reuse unless `EMBEDDING_API_KEY` is set separately.

## Common Use Cases

- Give AI coding assistants persistent project memory across sessions through MCP
- Build a private knowledge graph and vector memory backend for internal AI workflows
- Store, structure, and retrieve context from documents, notes, and development artifacts

## Dependencies for Cognee AI Memory Platform with MCP Hosting

- An OpenRouter API key for LLM access
- PostgreSQL with pgvector support (provisioned by the template)

### Deployment Dependencies

- Cognee docs: https://docs.cognee.ai/
- Cognee MCP quickstart: https://docs.cognee.ai/cognee-mcp/mcp-quickstart
- Railway template docs: https://docs.railway.com/templates/create
- OpenCode config schema: https://opencode.ai/config.json

### Implementation Details

The template deploys:
- `cognee-api` from the upstream image `cognee/cognee:1.6.8` with a `/health` healthcheck
- `cognee-mcp` from the upstream `cognee/cognee-mcp` image in API mode, exposed publicly at `/mcp`
- `Postgres` as the shared persistence layer for relational, graph, and vector data. Upstream cognee labels its Postgres graph adapter demo-grade and recommends a graph-native store such as Neo4j for heavy production workloads; this template favors one database over that.

Example OpenCode MCP configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "cognee": {
      "type": "remote",
      "url": "https://YOUR-MCP-DOMAIN.up.railway.app/mcp",
      "enabled": true
    }
  }
}
```

Claude Code: `claude mcp add --transport http cognee https://YOUR-MCP-DOMAIN.up.railway.app/mcp`

### Upgrading the API/MCP pair

Back up Postgres and retain the old image pair before updating. If raw files are needed for
re-ingestion or rollback, also archive `/cognee-storage` from the old API container: the standard
template has no API volume. Graph, vectors and metadata remain in Postgres, while raw files are
lost on API replacement. The standard graph provider is Postgres, so the Ladybug format change
does not apply. Image-only downgrade fails on a newer Alembic revision; rollback requires restoring
the pre-upgrade database backup and old images, plus raw files when needed. See the
[upgrade and rehearsal details](https://github.com/RockinPaul/cognee_railway_template/blob/main/CHANGELOG.md).

Leave `ALLOW_HTTP_REQUESTS` and `ALLOW_DATABASE_INGESTION` unset unless deliberately enabling
source ingestion on the API service. Explicit true still rejects private HTTP targets and Cognee's
own database. API-mode MCP `remember(data=...)` uploads strings as literal text rather than fetching
URLs/databases; never put a credential-bearing DSN in it. Use the HTTP API's explicit `raw_data`
route for source ingestion. No ingestion opt-in, embedding change or storage-topology change is
silently enabled by this update.

The populated upgrade/replacement/rollback rehearsal used Linux/amd64 and the actual Railway
PostgreSQL 18 SSL image, with old/new API-mode MCP queries and writes. Data/vector/schema identity
and TLS connections were checked. Model/3072-dimensional embedding replies were supplied by a
controlled local stub; no paid-provider or live Railway deployment verification is claimed.

## Why Deploy Cognee AI Memory Platform with MCP on Railway?

Railway is a singular platform to deploy your infrastructure stack. Railway will host your infrastructure so you don't have to deal with configuration, while allowing you to vertically and horizontally scale it.

By deploying Cognee AI Memory Platform with MCP on Railway, you are one step closer to supporting a complete full-stack application with minimal burden. Host your servers, databases, AI agents, and more on Railway.
