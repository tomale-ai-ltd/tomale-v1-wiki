---
type: decision
title: "scope-agent-context-per-tool"
project: tomale-rn-v1
status: accepted
date: 2026-10-23
related:
  - "[[knowledge-architecture]]"
---

---

# Decision: scope-agent-context-per-tool

## What we decided

Each tool gets a defined context. Claude Project knowledge: `Canonical/` **plus all decisions**, synced automatically by the daily pipeline (replacing the 37 hand-uploaded copies), so plain claude.ai chats without the desktop link stay current. Claude via the desktop link: whole vault and `Repos/` on demand; writes to the vault only. Cursor: repo natively, vault `Canonical/` as a second workspace folder, `tomale-project.mdc` (always) and `tomale-api.mdc` (`api/**`); writes raw session notes to `_raw/Chat Sessions/` only. Xano AI: Knowledge tab fed from `Canonical/backend-xano.md`. `specify-rules.mdc` is never edited (speckit regenerates it); its stale AsyncStorage-token line is fixed at its source in `specs/002-foundations-auth/plan.md`.

## Why

Copied docs drift. Loading too much context costs tokens and dilutes quality. Overwriting a speckit-generated file would break the spec-driven flow.

## Alternatives considered

Project knowledge limited to Tier 1 (rejected: plain chats would lose decision history). Point every tool at the whole vault (rejected: history and stale docs presented as authoritative).

## Trade-offs accepted

Claude Project knowledge has to be refreshed when Tier 1 changes materially.

## Workflow detail

Xano AI gets focused briefs naming tables and fields, and its output is checked against the published version in the `tomale-xano` mirror before pasting.

## Related notes

- [[knowledge-architecture]]
- [[2026-10-23-001]]
- [[adopt-repo-vault-ownership-split-for-project-knowledge]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[adopt-frontmatter-lifecycle-schema]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[retire-obsidian-llm-wiki-plugin]]
- [[version-the-vault-with-git]]
- [[defer-postman-suite-ci-until-suite-split]]
