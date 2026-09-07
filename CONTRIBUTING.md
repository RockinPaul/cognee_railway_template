# Contributing

This repo is the Railway template for cognee, not cognee itself. Product changes go to [topoteretes/cognee](https://github.com/topoteretes/cognee).

## What belongs here

- The two Dockerfiles and the image tags they pin
- Railway deployment docs and the marketplace overview
- `CHANGELOG.md` entries, especially upgrade steps for existing deployers

## Bumping cognee

1. Change the tag in `Dockerfile` to the new `cognee/cognee:<version>`. Check Docker Hub for a matching `cognee/cognee-mcp` tag; if none exists, use the newest `main-<sha>` and update `Dockerfile.mcp`.
2. Read the upstream release notes for schema or variable changes. If existing deployers must act, write it in `CHANGELOG.md`.
3. Deploy the branch to the reference project (see `RAILWAY_SETUP.md`) and verify `/health` on both services plus a `remember` → `recall` round trip over MCP.
4. If template settings or variables change, edit the template in the Railway dashboard before merging.
5. Merge to `main`. Railway notifies deployers.

## Networking policy

Service-to-service traffic uses Railway private domains (`*.railway.internal`). Public domains are only for MCP clients and people.
