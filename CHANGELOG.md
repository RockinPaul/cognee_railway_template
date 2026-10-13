# Changelog

## 2026-10 — cognee 1.6.4

- `cognee-api` runs `cognee/cognee:1.6.4` (was 1.5.4). `cognee-mcp` runs `cognee/cognee-mcp:main-f154b32`, the v1.6.4 release commit (was `main-e93a4f0`).
- Security fixes since 1.5.4: the default user no longer gets the public `default_password`; token signing secrets no longer fall back to the public `super_secret`; configuration reads and agent connections are scoped to their owner; Alembic no longer logs the database password. 1.6.4 also stops pgvector searches from selecting the vector column.
- Upstream removed the LanceDB compaction settings and `.env` file loading. This template uses neither: it runs on pgvector and sets everything as service variables.

### Upgrading an existing deployment

Your data stays, and in the default single-user setup (`REQUIRE_AUTHENTICATION=false`) there is nothing to change. **Back up Postgres first**: 1.6.4 adds two Alembic revisions (a dataset-listing index and the capability layer), and 1.5.4 cannot start against a database that has them. Verified locally with the template's variables: a 1.5.4 database with a stored memory upgraded in place, kept its graph, recalled the old memory through `/mcp` and stored a new one.

**If you turned authentication on:**

1. Set `FASTAPI_USERS_JWT_SECRET` on `cognee-api` to a long random value. 1.5.4 signed tokens with the public `super_secret`; 1.6.4 generates a secret at each start when the variable is unset, so tokens stop working on every restart (verified: 200 before a restart, 401 after; with the variable set, 200 after).
2. Log in again and put the new token in `API_TOKEN` on `cognee-mcp`. Tokens signed with `super_secret` are no longer accepted.
3. Change the default user's password if it is still `default_password`. Upgrades keep the password the account already has, and `DEFAULT_USER_PASSWORD` sets one only on an account that has none, so it does not replace the old one.

New deploys create the default user without a password (it cannot log in), so a fresh single-user deploy works unchanged.

## 2026-09 — cognee 1.5.4

**Breaking for existing deployments.** Read "Upgrading" below before applying this update.

- `cognee-api` runs the upstream image `cognee/cognee:1.5.4`. Previously this repo vendored a cognee 1.0.1 fork.
- `cognee-mcp` runs `cognee/cognee-mcp:main-e93a4f0` with Streamable HTTP at `/mcp`. Previously SSE at `/sse`.
- Removed: the vendored `cognee/` and `distributed/` trees, `pyproject.toml`, `uv.lock`, `entrypoint.sh`, `railway-template.json`, `railway.api.toml`, `railway.mcp.toml`, `tests/`, `examples/`.
- `railway.toml` stays for services created before Railway deprecated Config-as-Code. Railway stops reading it on 2026-12-01.
- New deploys default to `openrouter/openai/text-embedding-3-large` embeddings (GA, cheaper) instead of the `gemini-embedding-2-preview` model. **Existing deployments keep their embedding model.** Changing `EMBEDDING_MODEL` invalidates stored vectors and requires re-adding all data.
- New deploys set `GRAPH_DATABASE_NAME` and `VECTOR_DB_NAME`. Optional on existing deployments; they only silence a "falling back to the relational database configuration" warning.

### Upgrading an existing deployment

Your data stays. Railway's update rebuilds only `cognee-api` and `cognee-mcp`; it never touches the Postgres service or its volume.

**Back up Postgres first** (Railway → Postgres service → Backups → Create backup). The update is one-way: once 1.5.4 has migrated the database, the old 1.0.1 image cannot start against it (Alembic aborts with "Can't locate revision") and Railway's deployment rollback still reports success while the API answers 502. Rolling back means restoring the backup, then rolling back the deployment.

1. **Graph tables migrate themselves.** cognee 1.5.4 adds four provenance columns and a `graph_metadata` table to its Postgres graph store. Its startup migration chain does this automatically (`postgres_graph_provenance_columns`, idempotent `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`), and the relational schema migrates through Alembic at the same time. Verified on a 1.0.1 database: 429 nodes and 398 edges survived and were searchable afterwards. No SQL to run.

   Prefer a clean start instead? `DROP TABLE IF EXISTS graph_edge, graph_node, graph_metadata;` and re-add your content, or wipe the Postgres volume. Raw files were never persisted, so `cognify` cannot re-run on old data.
2. **`cognee-mcp` service.** The old template built the API image for this service. Set the variables `RAILWAY_DOCKERFILE_PATH=Dockerfile.mcp`, `TRANSPORT_MODE=http`, and `MCP_DISABLE_DNS_REBINDING_PROTECTION=true` (without it Railway's healthcheck gets HTTP 421 and the deploy fails), generate a public domain, and set the healthcheck path to `/health`. Point MCP clients at `https://<mcp-domain>/mcp`. `TRANSPORT_MODE=sse` at `/sse` still works if you prefer it. `MCP_ALLOWED_HOSTS` and `SERVE_URL` can be removed.
3. **`cognee-api` service.** If `EMBEDDING_API_KEY` is empty, set it to your OpenRouter key (or `${{LLM_API_KEY}}`). The old template said an empty value reuses `LLM_API_KEY`; with `LLM_PROVIDER=custom` it does not, and `add`/`cognify` fail with "Embedding connection test timed out". Optionally rename `ENVIRONMENT` to `ENV` and remove `HOST`; the old name is still accepted and `HOST` was never used.
4. Apply the update, then check `/health` on both services.
