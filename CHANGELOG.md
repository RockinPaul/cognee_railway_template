# Changelog

## 2026-11-17 — cognee 1.6.8 and MCP main-5870f15

- Advances API 1.6.6 to 1.6.8 and MCP `main-df2b4fa` to `main-5870f15` together. These are tested
  compatible builds, not the same source commit. Provider, embedding and storage defaults stay unchanged.
- The standard deployment uses Postgres/pgvector, not Ladybug/Kuzu. The flagged Ladybug format
  43→49 conversion therefore does not apply. Its PostgreSQL provenance columns/indexes were already
  present in the old 1.6.6 fixture; the upgrade preserves them rather than introducing them.
- Raw files remain ephemeral without an API volume. Back up Postgres **and** copy `/cognee-storage`
  before replacement if re-ingestion or complete rollback matters; graph/vector/metadata persistence
  is not raw-file persistence. This update adds no storage topology change.
- The 1.6.6 API cannot start on the new Alembic revision `e3f1a9c5b7d2`. Restore a consistent
  pre-upgrade logical backup and the old image pair for rollback; restore raw files as needed.
- API URL/database ingestion opt-ins remain unset. API-mode MCP string uploads are literal text,
  including URLs and DSNs. Use the explicit API source-ingestion route for deliberate fetching;
  never give MCP a credential-bearing DSN. Existing HTTP/database safety checks remain active.
- Corrects the authentication guidance: enabling backend auth and configuring an MCP backend key
  still delegates that key to anonymous MCP callers. Use private MCP exposure or an authenticated
  gateway. `COGNEE_API_KEY` plus the `x-api-key` auth scheme avoids a key in process arguments;
  stable JWT signing configuration is needed if using login tokens across replacement.

### Rehearsal scope

Verified populated old API/MCP → target pair on Linux/amd64 with real PostgreSQL/pgvector.
The initial PG17 matrix was supplemented with the actual Railway source image
`ghcr.io/railwayapp-templates/postgres-ssl:18` (resolved to PostgreSQL 18.6 / pgvector 0.8.7).
That PG18 baseline included two users, four datasets/documents, 16 graph nodes and 19 edges,
including a new write through the old API-mode MCP. Upgrade preserved the complete captured
application rows, vectors, eight provenance columns and six GIN indexes exactly. New writes,
API/MCP searches and full replacement passed; database connections negotiated TLS 1.3 with no
SSL-mode overrides, and the database certificate fingerprint persisted.

A separate logical backup restore into a fresh PG18 test volume, plus the baseline raw archive
and old image pair, restored identities/content, login, searches and new old-version writes.
The separate image-only downgrade failed at the newer Alembic revision; no reverse migration was
invented. Unset/false ingestion refusals, explicit local opt-ins and their safety refusals were
tested; API-mode MCP literal-upload and public-transport delegation behavior were verified directly.
An auth-enabled test variant checked 401s and stable JWT/API-key access across replacement without
changing this template's intentionally unauthenticated defaults.

Model and 3072-dimensional embedding responses came from a controlled local stub, not a paid
provider. No live data, Railway deployment/publication or Ladybug migration was used. The mutable
PG18 source tag was resolved for the rehearsal; it is not a claim about the immutable bits of an
older running production container. Docker's inherited image health probes still target port 8000;
the wrapper serves 8080, so verification used the actual `/health`, API and MCP endpoints rather
than treating Docker's health status as proof.

Earlier entries below are dated historical evidence; their `API_TOKEN` instructions only configure
backend access and must not be read as MCP transport authentication.

## 2026-11 — cognee 1.6.6

- `cognee-api` runs `cognee/cognee:1.6.6` (was 1.6.4). `cognee-mcp` runs `cognee/cognee-mcp:main-df2b4fa`, the v1.6.6 release commit (was `main-f154b32`).
- Security fixes since 1.6.4: prompt file reads are confined to their directory; the visualisation permission check is skipped only for the dataset owner; Cypher search types are off by default; certifi 2026.10.19 and refreshed CA bundles in the image.
- Upstream removed the filesystem session cache backend and moved fastembed models to the Hugging Face cache. This template uses neither: it runs on pgvector with an OpenAI-compatible embedding endpoint.

### Upgrading an existing deployment

Nothing to change. **Back up Postgres first**: 1.6.6 adds three Alembic revisions (pipeline run sessions, embedding token usage, and one that drops `run_info` data), so a rollback to 1.6.4 means restoring the backup. If you relied on Cypher search through the API, it is now opt-in upstream.

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
