---
type: decision
title: keep-agents-out-of-xano-no-mcp
project: tomale-rn-v1
status: accepted
date: 2026-10-24
related:
  - "[[knowledge-architecture]]"
  - "[[operating-model]]"
features:
  - X-process
  - X-security
---

# Decision: keep-agents-out-of-xano-no-mcp

## What we decided

No AI agent gets direct access to Xano, read or write, through Xano's MCP or CLI. Agents read the backend through the read-only GitHub mirror and the generated specs. Changes are drafted by Xano AI or Claude and published only by Kyle.

## Why

Kyle prefers a clear separation of concerns for the live backend. Agent-driven writes to the live workspace are a risk this project doesn't need, given the mirror gives agents the read access they need.

## Alternatives considered

Connect Cursor or Claude to Xano via its MCP (possible, rejected for now).

## Trade-offs accepted

Backend changes keep a human publish step; slightly slower loops.

## Workflow detail

Backend change workflow in [[operating-model]] §3.2.

## Related notes

- [[knowledge-architecture]]
- [[operating-model]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[adopt-frontmatter-lifecycle-schema]]
- [[adopt-order-of-authority-for-project-knowledge]]
- [[adopt-repo-vault-ownership-split-for-project-knowledge]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[defer-postman-suite-ci-until-suite-split]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[mirror-xano-workspace-to-github-read-only]]
- [[protect-speckit-and-generated-spec-documents]]
- [[retire-obsidian-llm-wiki-plugin]]
- [[scope-agent-context-per-tool]]
- [[version-the-vault-with-git]]
