# Deploy and Host Cognee AI Memory Platform with MCP on Railway

Cognee AI Memory Platform with MCP combines a private Cognee backend, durable Postgres + pgvector storage, and a public MCP service so AI tools can store, structure, and retrieve memory across sessions. The template runs the upstream cognee 1.5.4 images with OpenRouter-backed models and exposes the MCP server over Streamable HTTP for client integrations.

## About Hosting Cognee AI Memory Platform with MCP

Hosting this template deploys three connected services: `cognee-api` as the private backend, `cognee-mcp` as the public MCP layer, and PostgreSQL as the shared relational, graph, and vector store. Railway handles provisioning, private networking, and runtime configuration, while the template wires the MCP service to the backend over the internal network. The result is a single-user memory stack that supports ingestion, Cognify processing, search, and MCP tool access from clients like OpenCode and Claude Code. You only need to provide an LLM API key, and optionally a separate embedding key.

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
- `cognee-api` from the upstream image `cognee/cognee:1.5.4` with a `/health` healthcheck
- `cognee-mcp` from the upstream `cognee/cognee-mcp` image in API mode, exposed publicly at `/mcp`
- `Postgres` as the shared persistence layer for relational, graph, and vector data

Example OpenCode MCP configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "cognee": {
      "type": "remote",
      "url": "https://<cognee-mcp-service>.up.railway.app/mcp",
      "enabled": true
    }
  }
}
```

Claude Code: `claude mcp add --transport http cognee https://<cognee-mcp-service>.up.railway.app/mcp`

## Why Deploy Cognee AI Memory Platform with MCP on Railway?

Railway is a singular platform to deploy your infrastructure stack. Railway will host your infrastructure so you don't have to deal with configuration, while allowing you to vertically and horizontally scale it.

By deploying Cognee AI Memory Platform with MCP on Railway, you are one step closer to supporting a complete full-stack application with minimal burden. Host your servers, databases, AI agents, and more on Railway.
