# Railway Setup (maintainers)

Two things live on Railway and are edited separately:

1. **The published template** `cognee-ai-memory-p-1`: Workspace → Templates → "Cognee AI Memory Platform with MCP". This is what deployers get. Its services attach directly to this repo's `main` branch.
2. **The reference project** `cognee-railway-template`: a normal project used to test changes. Editing it does not change the template.

Railway deprecated `railway.toml` / `railway.json` config. New services ignore them, and existing ones stop reading them on 2026-12-01. Service settings therefore live in the template definition, not in this repo.

## Template definition

`cognee-api`
- Source: `https://github.com/RockinPaul/cognee_railway_template`, branch `main`
- Healthcheck path `/health`, timeout 240, restart `ON_FAILURE`
- Public domain enabled
- Variables: see the "Variables" table below

`cognee-mcp`
- Source: same repo, branch `main`
- Variable `RAILWAY_DOCKERFILE_PATH=Dockerfile.mcp` (required, otherwise Railway builds the API `Dockerfile`)
- Healthcheck path `/health`, timeout 240
- Public domain enabled, target port 8080
- Variables: `PORT=8080`, `TRANSPORT_MODE=http`, `API_URL=http://${{cognee-api.RAILWAY_PRIVATE_DOMAIN}}:8080`, `MCP_DISABLE_DNS_REBINDING_PROTECTION=true`, `API_TOKEN=` (optional)
- Why the DNS-rebinding flag: Railway's healthcheck probes the container from an internal address whose `Host` header is not the public domain. With the check on, every probe gets HTTP 421 and the deploy fails. Railway's edge already routes only the configured domain to the service, so the check adds nothing here. `MCP_ALLOWED_HOSTS` is then unused and can be dropped.

`Postgres`
- Railway's `postgres-ssl` image with a volume at `/var/lib/postgresql/data`. Unchanged.

### Variables for `cognee-api`

| Variable | Value |
|---|---|
| `LLM_API_KEY` | user supplied |
| `LLM_PROVIDER` | `custom` |
| `LLM_ENDPOINT` | `https://openrouter.ai/api/v1` |
| `LLM_MODEL` | `openrouter/openai/gpt-4o-mini` |
| `LLM_INSTRUCTOR_MODE` | `json_schema_mode` |
| `EMBEDDING_PROVIDER` | `litellm` |
| `EMBEDDING_ENDPOINT` | `https://openrouter.ai/api/v1` |
| `EMBEDDING_MODEL` | `openrouter/google/gemini-embedding-2-preview` |
| `EMBEDDING_DIMENSIONS` | `3072` |
| `EMBEDDING_API_KEY` | `${{LLM_API_KEY}}` (same-service reference; deployers override for a separate key). Must not be empty: with `LLM_PROVIDER=custom` there is no fallback to the LLM key. |
| `DB_PROVIDER` | `postgres` |
| `DB_HOST` / `DB_PORT` / `DB_USERNAME` / `DB_PASSWORD` / `DB_NAME` | `${{Postgres.PGHOST}}` / `PGPORT` / `PGUSER` / `PGPASSWORD` / `PGDATABASE` |
| `GRAPH_DATABASE_PROVIDER` | `postgres` |
| `GRAPH_DATABASE_URL` | `postgresql+asyncpg://${{Postgres.PGUSER}}:${{Postgres.PGPASSWORD}}@${{Postgres.PGHOST}}:${{Postgres.PGPORT}}/${{Postgres.PGDATABASE}}` |
| `GRAPH_DATABASE_HOST` / `PORT` / `USERNAME` / `PASSWORD` | same `${{Postgres.*}}` references |
| `VECTOR_DB_PROVIDER` | `pgvector` |
| `VECTOR_DB_URL` | `postgresql://${{Postgres.PGUSER}}:${{Postgres.PGPASSWORD}}@${{Postgres.PGHOST}}:${{Postgres.PGPORT}}/${{Postgres.PGDATABASE}}` |
| `VECTOR_DB_HOST` / `PORT` / `USERNAME` / `PASSWORD` | same `${{Postgres.*}}` references |
| `VECTOR_DATASET_DATABASE_HANDLER` | `pgvector` |
| `ENABLE_BACKEND_ACCESS_CONTROL` | `false` |
| `REQUIRE_AUTHENTICATION` | `false` |
| `ENV` | `prod` |
| `PORT` | `8080` (so `API_URL` is deterministic) |
| `CORS_ALLOWED_ORIGINS` | `*` |

## Editing the template

Open the template in the dashboard editor, change services or variables, save. The template code and deploy URL stay the same. Do not use `railway templates create` for this: it produces a new template with a new code.

Marketplace text comes from `TEMPLATE_OVERVIEW.md`:

```bash
railway templates publish cognee-ai-memory-p-1 --readme-file TEMPLATE_OVERVIEW.md
```

Repo changes merged to `main` trigger Railway's opt-in update notification for every deployer. Template-definition changes reach only new deploys, so anything an existing deployer must change by hand goes into `CHANGELOG.md`.

## Rebuilding the reference project

```bash
railway login
railway link -p cognee-railway-template -e production
```

Then per service in the dashboard: `cognee-api` source = this repo on the branch under test; `cognee-mcp` source = this repo with `RAILWAY_DOCKERFILE_PATH=Dockerfile.mcp`; healthchecks `/health`; variables as above. Deploy Postgres first.

Verify:

- `https://<api-domain>/health` returns 200
- `https://<mcp-domain>/health` returns 200
- an MCP client connected to `https://<mcp-domain>/mcp` can run `remember` then `recall`
- `railway logs -s cognee-api` shows `Database migrations done` and an `auth posture` line
