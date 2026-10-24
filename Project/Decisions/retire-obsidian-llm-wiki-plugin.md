---
type: decision
title: retire-obsidian-llm-wiki-plugin
project: tomale-rn-v1
status: accepted
date: 2026-10-23
related:
  - "[[knowledge-architecture]]"
---

---

# Decision: retire-obsidian-llm-wiki-plugin

## What we decided

Retire the Obsidian LLM-wiki plugin and delete its generated `wiki/` folder (584 stub notes plus a 700 KB `knowledge.json`) once the vault is under git. The knowledge base itself stays; Claude and Cursor are the query layer.

## Why

The plugin's gpt-4o-mini answers were poor (often blank), its stubs were thin and duplicated, and they could pollute agent search with low-authority content built from stale sources.

## Alternatives considered

Keep the plugin and exclude `wiki/` from other agents (rejected: low value, upkeep cost). Zip instead of delete (unnecessary once git history holds it).

## Trade-offs accepted

No in-Obsidian chat. Recoverable from git history if ever wanted.

## Workflow detail

Ask Claude (desktop link) or Cursor questions about the project instead.

## Related notes

- [[knowledge-architecture]]
- [[2026-10-23-001]]
- [[adopt-repo-vault-ownership-split-for-project-knowledge]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[adopt-frontmatter-lifecycle-schema]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[scope-agent-context-per-tool]]
- [[version-the-vault-with-git]]
- [[defer-postman-suite-ci-until-suite-split]]
