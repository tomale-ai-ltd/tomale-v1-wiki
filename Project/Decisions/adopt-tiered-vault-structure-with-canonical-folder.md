---
type: decision
title: adopt-tiered-vault-structure-with-canonical-folder
project: tomale-rn-v1
status: accepted
date: 2026-10-23
supersedes:
  - "[[create-architecture-folder-for-system-flow-docs]]"
related:
  - "[[knowledge-architecture]]"
---

---

# Decision: adopt-tiered-vault-structure-with-canonical-folder

## What we decided

The vault is organised in three tiers. Tier 1, `Canonical/`: all declarative (source-of-truth) docs (`CURRENT.md`, backend-xano, security model, test suite, pre-launch checklist, roadmap, `v1-feature-map`, architecture flows, PRDs), plus read-only `Repos/<repo>/` views (symlinks into `tomale-rn-test`; a clone of the `tomale-xano` mirror). Tier 2: `Project/Decisions/`. Tier 3: sessions (kept where they are), raw notes, web clippings, research (including the CfI proposals) and `Project/_archive/` (superseded Plan/Stack/Cursor baseline). Every existing folder is mapped in [[knowledge-architecture]] §5.

## Why

The April–May baseline docs were treated as authoritative by agents but contradicted by Phase 1. Separating what is true now from how we got here gives agents a small, trustworthy context and keeps history searchable.

## Alternatives considered

Tag documents where they are without moving them (rejected: folder-based tiers are easier for tools to scope). The names `Current/` and `Repo/` (replaced by `Canonical/` and `Repos/<repo>/`, which allow for future repos that rely on the same sources of truth).

## Trade-offs accepted

A one-off move of files with link rewriting. Living docs need maintaining (`last_verified`).

## Workflow detail

Agents load Tier 1 by default and Tier 2 through Claude Project knowledge; Tier 3 only when asked. No hard word cap: `CURRENT.md` is the entry point and links out rather than repeating.

## Related notes

- [[knowledge-architecture]]
- [[2026-10-23-001]]
- [[adopt-repo-vault-ownership-split-for-project-knowledge]]
- [[adopt-frontmatter-lifecycle-schema]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[retire-obsidian-llm-wiki-plugin]]
- [[scope-agent-context-per-tool]]
- [[version-the-vault-with-git]]
- [[defer-postman-suite-ci-until-suite-split]]
