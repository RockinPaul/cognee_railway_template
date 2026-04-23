<div align="center">
  <a href="https://github.com/topoteretes/cognee">
    <img src="https://raw.githubusercontent.com/topoteretes/cognee/refs/heads/dev/assets/cognee-logo-transparent.png" alt="Cognee Logo" height="60">
  </a>

  <br />

  Cognee - Build AI memory with a Knowledge Engine that learns

  <p align="center">
  <a href="https://www.youtube.com/watch?v=8hmqS2Y5RVQ&t=13s">Demo</a>
  .
  <a href="https://docs.cognee.ai/">Docs</a>
  .
  <a href="https://cognee.ai">Learn More</a>
  ·
  <a href="https://discord.gg/NQPKmU5CCg">Join Discord</a>
  ·
  <a href="https://www.reddit.com/r/AIMemory/">Join r/AIMemory</a>
  .
  <a href="https://github.com/topoteretes/cognee-community">Community Plugins & Add-ons</a>
  </p>


  [![GitHub forks](https://img.shields.io/github/forks/topoteretes/cognee.svg?style=social&label=Fork&maxAge=2592000)](https://GitHub.com/topoteretes/cognee/network/)
  [![GitHub stars](https://img.shields.io/github/stars/topoteretes/cognee.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/topoteretes/cognee/stargazers/)
  [![GitHub commits](https://badgen.net/github/commits/topoteretes/cognee)](https://GitHub.com/topoteretes/cognee/commit/)
  [![GitHub tag](https://badgen.net/github/tag/topoteretes/cognee)](https://github.com/topoteretes/cognee/tags/)
  [![Downloads](https://static.pepy.tech/badge/cognee)](https://pepy.tech/project/cognee)
  [![License](https://img.shields.io/github/license/topoteretes/cognee?colorA=00C586&colorB=000000)](https://github.com/topoteretes/cognee/blob/main/LICENSE)
  [![Contributors](https://img.shields.io/github/contributors/topoteretes/cognee?colorA=00C586&colorB=000000)](https://github.com/topoteretes/cognee/graphs/contributors)
  <a href="https://github.com/sponsors/topoteretes"><img src="https://img.shields.io/badge/Sponsor-❤️-ff69b4.svg" alt="Sponsor"></a>

<p>
  <a href="https://trendshift.io/repositories/13955" target="_blank" style="display:inline-block;">
    <img src="https://trendshift.io/api/badge/repositories/13955" alt="topoteretes%2Fcognee | Trendshift" width="250" height="55" />
  </a>
</p>

Use our knowledge engine to build personalized and dynamic memory for AI Agents.

  <p align="center">
  🌐 Available Languages
  :
  <!-- Keep these links. Translations will automatically update with the README. -->
  <a href="https://www.readme-i18n.com/topoteretes/cognee?lang=de">Deutsch</a> |
  <a href="https://www.readme-i18n.com/topoteretes/cognee?lang=es">Español</a> |
  <a href="https://www.readme-i18n.com/topoteretes/cognee?lang=fr">Français</a> |
  <a href="https://www.readme-i18n.com/topoteretes/cognee?lang=ja">日本語</a> |
  <a href="README_ko.md">한국어</a> |
  <a href="https://www.readme-i18n.com/topoteretes/cognee?lang=pt">Português</a> |
  <a href="https://www.readme-i18n.com/topoteretes/cognee?lang=ru">Русский</a> |
  <a href="https://www.readme-i18n.com/topoteretes/cognee?lang=zh">中文</a>
  </p>


<div style="text-align: center">
  <img src="https://raw.githubusercontent.com/topoteretes/cognee/refs/heads/main/assets/cognee_benefits.png" alt="Why cognee?" width="80%" />
</div>
</div>




## About Cognee

Cognee is an open-source knowledge engine that lets you ingest data in any format or structure and continuously learns to provide the right context for AI agents. It combines vector search, graph databases and cognitive science approaches to make your documents both searchable by meaning and connected by relationships as they change and evolve.



:star: _Help us reach more developers and grow the cognee community. Star this repo!_

:books: _Check our detailed [documentation](https://docs.cognee.ai/getting-started/installation#environment-configuration) for setup and configuration._

:crab: _Available as a plugin for your OpenClaw — [cognee-openclaw](https://www.npmjs.com/package/@cognee/cognee-openclaw)_

✴️ _Available as a plugin for your Claude Code — [claude-code-plugin](https://github.com/topoteretes/cognee-integrations/tree/main/integrations/claude-code)_


Cognee memory plugin


### Why use Cognee:

- Knowledge infrastructure — unified ingestion, graph/vector search, runs locally, ontology grounding, multimodal
- Persistent and Learning Agents - learn from feedback, context management, cross-agent knowledge sharing
- Reliable and Trustworthy Agents - agentic user/tenant isolation, traceability, OTEL collector, audit traits

### Product Features

<p align="center">
  <img src="assets/cognee_products.png" alt="Cognee Products" width="80%" />
</p>

## Basic Usage & Feature Guide

To learn more, [check out this short, end-to-end Colab walkthrough](https://colab.research.google.com/drive/12Vi9zID-M3fpKpKiaqDBvkk98ElkRPWy?usp=sharing) of Cognee's core features.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/12Vi9zID-M3fpKpKiaqDBvkk98ElkRPWy?usp=sharing)

## Quickstart

Let’s try Cognee in just a few lines of code.

### Prerequisites

- Python 3.10 to 3.13

### Step 1: Install Cognee

You can install Cognee with **pip**, **poetry**, **uv**, or your preferred Python package manager.

```bash
uv pip install cognee
```

### Step 2: Configure the LLM
```python
import os
os.environ["LLM_API_KEY"] = "YOUR OPENAI_API_KEY"
```
Alternatively, create a `.env` file using our [template](https://github.com/topoteretes/cognee/blob/main/.env.template).

To integrate other LLM providers, see our [LLM Provider Documentation](https://docs.cognee.ai/setup-configuration/llm-providers).

### Step 3: Run the Pipeline

Cognee's API gives you four operations — `remember`, `recall`, `forget`, and `improve`:

```python
import cognee
import asyncio


async def main():
    # Store permanently in the knowledge graph (runs add + cognify + improve)
    await cognee.remember("Cognee turns documents into AI memory.")

    # Store in session memory (fast cache, syncs to graph in background)
    await cognee.remember("User prefers detailed explanations.", session_id="chat_1")

    # Query with auto-routing (picks best search strategy automatically)
    results = await cognee.recall("What does Cognee do?")
    for result in results:
        print(result)

    # Query session memory first, fall through to graph if needed
    results = await cognee.recall("What does the user prefer?", session_id="chat_1")
    for result in results:
        print(result)

    # Delete when done
    await cognee.forget(dataset="main_dataset")


if __name__ == '__main__':
    asyncio.run(main())

```

### Use the Cognee CLI

```bash
cognee-cli remember "Cognee turns documents into AI memory."

cognee-cli recall "What does Cognee do?"

cognee-cli forget --all
```

To open the local UI, run:
```bash
cognee-cli -ui
```

## Use with AI Agents

### Claude Code

Install the [Cognee memory plugin](https://github.com/topoteretes/cognee-integrations/tree/main/integrations/claude-code) to give Claude Code persistent memory across sessions. The plugin automatically captures tool calls into session memory via hooks and syncs to the permanent knowledge graph at session end.

**Setup:**

```bash
# Install cognee
pip install cognee

# Configure
export LLM_API_KEY="your-openai-key"

# Clone the plugin
git clone https://github.com/topoteretes/cognee-integrations.git

# Enable it (add to ~/.zshrc for permanent use)
claude --plugin-dir ./cognee-integrations/integrations/claude-code
```

Or connect to Cognee Cloud instead of running locally:

```bash
export COGNEE_SERVICE_URL="https://your-instance.cognee.ai"
export COGNEE_API_KEY="ck_..."
```

The plugin hooks into Claude Code's lifecycle — `SessionStart` initializes memory, `PostToolUse` captures actions, `UserPromptSubmit` injects relevant context, `PreCompact` preserves memory across context resets, and `SessionEnd` bridges session data into the permanent graph.

### Hermes Agent

Enable Cognee as the memory provider in [Hermes Agent](https://github.com/NousResearch/hermes-agent) for session-aware knowledge graph memory with auto-routing recall.

**Setup:**

```yaml
# ~/.hermes/config.yaml
memory:
  provider: cognee
```

```bash
export LLM_API_KEY="your-openai-key"
hermes  # start chatting — session memory and graph persistence are automatic
```

Or run `hermes memory setup` and select Cognee. For Cognee Cloud, set `COGNEE_SERVICE_URL` and `COGNEE_API_KEY` in `~/.hermes/.env`.


### Connect to Cognee Cloud

Point any Python agent at a managed Cognee instance — all SDK calls route to the cloud:

```python
import cognee

await cognee.serve(url="https://your-instance.cognee.ai", api_key="ck_...")

await cognee.remember("important context")
results = await cognee.recall("what happened?")

await cognee.disconnect()
```

## Examples

Browse more examples in the [`examples/`](examples/) folder — demos, guides, custom pipelines, and database configurations.

**Use Case 1 — Customer Support Agent**

```python
Goal: Resolve customer issues using their personal data across finance, support, and product history.

User: "My invoice looks wrong and the issue is still not resolved."

Cognee tracks: past interactions, failed actions, resolved cases, product history

# Agent response:
Agent: "I found 2 similar billing cases resolved last month.
        The issue was caused by a sync delay between payment
        and invoice systems — a fix was applied on your account."

# What happens under the hood:
- Unifies data sources from various company channels
- Reconstructs the interaction timeline and tracks outcomes
- Retrieves similar resolved cases
- Maps to the best resolution strategy
- Updates memory after execution so the agent never repeats the same mistake
```

**Use Case 2 — Expert Knowledge Distillation (SQL Copilot)**

```python
Goal: Help junior analysts solve tasks by reusing expert-level queries, patterns, and reasoning.

User: "How do I calculate customer retention for this dataset?"

Cognee tracks: expert SQL queries, workflow patterns, schema structures, successful implementations

# Agent response:
Agent: "Here's how senior analysts solved a similar retention query.
        Cognee matched your schema to a known structure and adapted
        the expert's logic to fit your dataset."

# What happens under the hood:
- Extracts and stores patterns from expert SQL queries and workflows
- Maps the current schema to previously seen structures
- Retrieves similar tasks and their successful implementations
- Adapts expert reasoning to the current context
- Updates memory with new successful patterns so junior analysts perform at near-expert level
```

## Deploy Cognee

> **Note:** This repository is a deployment-focused fork of [topoteretes/cognee](https://github.com/topoteretes/cognee) optimized for Railway. It includes `railway.toml`, `railway-template.json`, and `Dockerfile.mcp` in the root so Railway can provision the documented production shape: a private `cognee-api` backend, a public `cognee-mcp` service in API/SSE mode, and managed Postgres. For full documentation, examples, and community resources, see the upstream repository.

Use [Cognee Cloud](https://www.cognee.ai) for a fully managed experience, or self-host with one of the 1-click deployment configurations below.

| Platform | Best For | Command |
|----------|----------|---------|
| **Cognee Cloud** | Managed service, no infrastructure to maintain | [Sign up](https://www.cognee.ai) or `await cognee.serve()` |
| **Modal** | Serverless, auto-scaling, GPU workloads | `bash distributed/deploy/modal-deploy.sh` |
| **Railway** | Simplest PaaS, native Postgres | `railway init && railway up` |
| **Fly.io** | Edge deployment, persistent volumes | `bash distributed/deploy/fly-deploy.sh` |
| **Render** | Simple PaaS with managed Postgres | Deploy to Render button |
| **Daytona** | Cloud sandboxes (SDK or CLI) | See `distributed/deploy/daytona_sandbox.py` |

See the [`distributed/`](distributed/) folder for deploy scripts, worker configurations, and additional details.

### Railway MCP Endpoint

The Railway template deploys:

- `cognee-api` as the private Cognee backend
- `cognee-mcp` as the public MCP service in API/SSE mode
- `postgres` for the relational, graph, and vector data stores

After deployment, point OpenCode or another MCP client at the public `cognee-mcp` domain with the `/sse` suffix:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "cognee": {
      "type": "remote",
      "url": "https://<cognee-mcp-service>.up.railway.app/sse",
      "enabled": true,
      "oauth": false
    }
  }
}
```

The `cognee-mcp` service talks to the private `cognee-api` service over Railway internal networking using `API_URL=http://cognee-api.railway.internal:8000`, matching the documented production setup.

### Railway Safe Environment Policy

Use private Railway networking for all service-to-service communication inside the same Railway project and environment.

Use internal/private values for:

- `DB_HOST`
- `GRAPH_DATABASE_HOST`
- `VECTOR_DB_HOST`
- `GRAPH_DATABASE_URL`
- `VECTOR_DB_URL`
- `API_URL` from `cognee-mcp` to `cognee-api`

Preferred internal hosts:

- `postgres.railway.internal`
- `cognee-api.railway.internal`
- `cognee-mcp.railway.internal`

Use public values only for:

- end-user and client connections
- OpenCode / Claude Code / MCP client configuration
- local debugging from outside Railway
- direct laptop access to Postgres via Railway TCP proxy

Public-only examples:

- `RAILWAY_PUBLIC_DOMAIN`
- `RAILWAY_STATIC_URL`
- `RAILWAY_SERVICE_COGNEE_API_URL`
- `RAILWAY_SERVICE_COGNEE_MCP_URL`
- `SERVE_URL`
- `DATABASE_PUBLIC_URL`
- `RAILWAY_TCP_PROXY_DOMAIN`
- `RAILWAY_TCP_PROXY_PORT`

Do not use public proxy/database URLs for internal runtime traffic between Railway services. They are slower and may incur egress/network charges.

### Railway Template Summary

Template name:

- `Cognee AI Memory Platform`

Short description:

- Deploy Cognee on Railway with a private backend API, a public MCP service in API/SSE mode, and managed Postgres + pgvector.

What the template provisions:

- `cognee-api` backend service
- `cognee-mcp` public MCP service
- `postgres` managed database

What users must provide:

- `LLM_API_KEY`
- optionally `EMBEDDING_API_KEY` if they do not want to reuse `LLM_API_KEY`

Default model choice:

- `openrouter/openai/gpt-4o-mini` is the reliable default for full Cognify pipelines
- `openrouter/google/gemma-4-26b-a4b-it` can still be used as an advanced override, but it is not the publishable default

### Final Publish Checklist

- `cognee-api /health` returns `200`
- `cognee-mcp /health` returns `200`
- `cognee-mcp /sse` returns `200`
- login works on the backend
- `add -> cognify -> search` works on a fresh dataset
- Postgres shows dataset persistence and nonzero graph data
- OpenCode connects to the MCP server successfully
- OpenCode can execute a real Cognee tool call successfully

## Latest News

[![Watch Demo](https://img.youtube.com/vi/8hmqS2Y5RVQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=8hmqS2Y5RVQ&t=13s)


## Community & Support

### Contributing
We welcome contributions from the community! Your input helps make Cognee better for everyone. See [`CONTRIBUTING.md`](CONTRIBUTING.md) to get started.

### Code of Conduct

We're committed to fostering an inclusive and respectful community. Read our [Code of Conduct](https://github.com/topoteretes/cognee/blob/main/CODE_OF_CONDUCT.md) for guidelines.

## Research & Citation

We recently published a research paper on optimizing knowledge graphs for LLM reasoning:

```bibtex
@misc{markovic2025optimizinginterfaceknowledgegraphs,
      title={Optimizing the Interface Between Knowledge Graphs and LLMs for Complex Reasoning},
      author={Vasilije Markovic and Lazar Obradovic and Laszlo Hajdu and Jovan Pavlovic},
      year={2025},
      eprint={2505.24478},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2505.24478},
}
```
