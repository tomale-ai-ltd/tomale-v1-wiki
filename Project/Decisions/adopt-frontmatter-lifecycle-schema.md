---
type: decision
title: adopt-frontmatter-lifecycle-schema
project: tomale-rn-v1
status: accepted
date: 2026-10-23
related:
  - "[[knowledge-architecture]]"
features:
  - X-process
---

# Decision: adopt-frontmatter-lifecycle-schema

## What we decided

A standard frontmatter for Tier 1 docs and decisions: `type` (fixed list), `title`, `project`, `status` (docs: draft/current/historical; decisions: proposed/accepted/superseded), `version` (living docs, plans, PRDs), `date`, `last_verified`, `owner` (vault/repo/generated), `supersedes`/`superseded_by`, `related` (quoted wikilinks), `features` (V1 feature ids) and `affects` (the canonical docs, protected specs and backend objects a decision changes, used for impact detection and the weekly check), optional controlled `tags`. Decisions are never versioned: they are superseded. Wikilinks use the filename only.

## Why

All 77 decisions said `status: current`, 14 of 16 Plan files had no frontmatter, and 48 links were broken by folder paths. Agents use frontmatter for filtering (skip superseded/historical) and links for following context.

## Alternatives considered

Rely on Obsidian Dataview views (rejected: agents read raw markdown, not rendered views).

## Trade-offs accepted

A scripted backfill that needs a manual review; a little more discipline when writing notes.

## Workflow detail

New notes use the schema; the decision-note automation writes it; the weekly staleness check uses `last_verified`.

## Related notes

- [[knowledge-architecture]]
- [[2026-10-23-001]]
- [[adopt-repo-vault-ownership-split-for-project-knowledge]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[retire-obsidian-llm-wiki-plugin]]
- [[scope-agent-context-per-tool]]
- [[version-the-vault-with-git]]
- [[defer-postman-suite-ci-until-suite-split]]
