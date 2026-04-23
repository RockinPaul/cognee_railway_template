# Contributing to the Cognee Railway Deployment Template

This repository is not the full upstream Cognee product repository.

It is a deployment-focused fork that exists to maintain a working Railway template and the minimum code and configuration required to deploy:

- `cognee-api`
- `cognee-mcp`
- `postgres`

For product development, feature work, and upstream community contributions, use the main Cognee repository:

- `https://github.com/topoteretes/cognee`

## What belongs in this repo

Changes are appropriate here if they improve one of the following:

- Railway deployment reliability
- Railway template correctness
- MCP production deployment shape on Railway
- backend and MCP service configuration defaults
- deployment documentation for this Railway-focused fork
- small code fixes required to make the deployment actually work on Railway

Examples:

- `railway-template.json` fixes
- `railway.toml` fixes
- `Dockerfile` or `Dockerfile.mcp` changes required for Railway
- README / deployment guide updates
- narrow runtime fixes that unblock `add -> cognify -> search`
- narrow MCP fixes that unblock OpenCode/Claude Code connectivity

## What does not belong in this repo

Please send these changes to the upstream Cognee repository instead:

- general product features
- non-Railway deployment work
- broad API redesigns
- unrelated graph/vector/database refactors
- upstream community or SDK documentation changes not specific to this fork

## Contribution workflow for this repo

1. Start from the current default branch of this repository.
2. Keep changes focused on deployment, template, or deployment-critical runtime behavior.
3. Prefer the smallest change that fixes the Railway or MCP issue.
4. Update documentation when behavior or required configuration changes.
5. Verify the relevant deployment path before considering the change complete.

## Required verification

For deployment-affecting changes, verify as many of these as apply:

- `cognee-api /health` returns `200`
- `cognee-mcp /health` returns `200`
- `cognee-mcp /sse` returns `200` in API/SSE mode
- login works on the backend
- `add -> cognify -> search` works on a fresh dataset
- OpenCode connects to MCP successfully
- OpenCode can execute at least one real Cognee MCP tool call
- Postgres shows dataset persistence and nonzero graph data after a successful smoke test

For repo-only changes, at minimum verify:

- changed JSON parses successfully
- changed Python files compile
- changed tests compile and, where relevant, pass

## Safe environment policy

Inside Railway, always prefer private/internal service-to-service networking.

Use internal hosts for:

- `DB_HOST`
- `GRAPH_DATABASE_HOST`
- `VECTOR_DB_HOST`
- `GRAPH_DATABASE_URL`
- `VECTOR_DB_URL`
- `API_URL`

Use public URLs only for:

- end-user access
- OpenCode / Claude Code / MCP client configuration
- local debugging from outside Railway
- direct laptop access to Postgres via Railway TCP proxy

## Model defaults for this fork

This fork uses a reliability-first default model choice for Cognify:

- default LLM model: `openrouter/openai/gpt-4o-mini`
- default embedding model: `openrouter/google/gemini-embedding-2-preview`

`openrouter/google/gemma-4-26b-a4b-it` may still be used as an advanced override, but it is not the stable default for this publishable Railway template.

## Important files in this repo

- `railway-template.json` — production Railway template
- `railway.toml` — backend deploy config
- `Dockerfile` — backend image
- `Dockerfile.mcp` — MCP wrapper image for Railway
- `README.md` — deployment-focused docs for this fork
- `distributed/deploy/README.md` — upstream-style deploy notes with Railway references

## Getting help

If you are unsure whether a change belongs here or upstream:

- open an issue in this fork for Railway/template-specific work
- use the upstream Cognee repo for general product questions and feature contributions
