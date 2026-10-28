---
type: decision
title: adopt-repo-vault-ownership-split-for-project-knowledge
project: tomale-rn-v1
status: accepted
date: 2026-10-23
related:
  - "[[knowledge-architecture]]"
features:
  - X-process
---

# Decision: adopt-repo-vault-ownership-split-for-project-knowledge

## What we decided

Every document has one owner. The Cursor repo (`tomale-rn-test`) owns the frontend engineering specs: the constitution, speckit feature specs/plans/tasks, foundation PRDs, and the generated data model and OpenAPI contract. The vault owns product (feature PRDs), backend (Xano) design, decisions, architecture explanations and history. The vault's `Project/Cursor` copies of `constitution`, `data-model`, `api-spec` are retired. Decisions made outside Cursor that affect repo-owned specs are queued in `Current/repo-sync.md` and applied by a Cursor agent. Claude never edits the repo.

## Why

The constitution and data model existed in both places, identical and frozen since November 2025 / April 2026, so neither could be trusted. Specs that change with code belong in the same commit as the code; backend design has no repo, so the vault is its only home.

## Alternatives considered

Vault as master for everything, synced into the repo (rejected: Cursor and speckit edit specs in place, so syncing would fight the speckit flow). Keep both copies (rejected: the drift was already there).

## Trade-offs accepted

Repo changes that come from chat decisions go through a queue and a Cursor step instead of being made directly.

## Workflow detail

When a session decides something that affects a repo spec, add an item to `repo-sync.md`. In Cursor: "apply the open items in repo-sync.md". Vault-side, repo specs are read through `Repo/` symlinks.

## Related notes

- [[knowledge-architecture]]
- [[2026-10-23-001]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[adopt-frontmatter-lifecycle-schema]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[retire-obsidian-llm-wiki-plugin]]
- [[scope-agent-context-per-tool]]
- [[version-the-vault-with-git]]
- [[defer-postman-suite-ci-until-suite-split]]
