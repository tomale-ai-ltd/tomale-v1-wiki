---
type: decision
title: "add-propose-only-reconcile-and-staleness-automations"
project: tomale-rn-v1
status: accepted
date: 2026-10-23
related:
  - "[[knowledge-architecture]]"
---

---

# Decision: add-propose-only-reconcile-and-staleness-automations

## What we decided

The two nightly tasks are replaced by one **daily knowledge pipeline at 17:00 on weekdays**, which runs in order: `git pull` of the Xano mirror clone → session notes from unprocessed raw notes (from Claude and Cursor) → decision notes → **reconcile** (proposed canonical edits to `Canonical/pending-updates.md`, repo-owned changes to `Canonical/repo-sync.md`) → sync of changed canonical docs and decisions to Claude Project knowledge. Every step works in catch-up mode (everything unprocessed, not just today). A weekly staleness check flags canonical docs not verified in 30 days, broken links, and decisions still `proposed` after 14 days. Automations never edit canonical docs or repos.

## Why

Decisions were piling up without being promoted into the baseline docs, which is how the drift happened. Date-filtered runs silently did nothing when the Mac was off or dates didn't match (9 Oct). Unsupervised edits to authoritative docs would just bring the drift back.

## Alternatives considered

Let the automation edit living docs directly (rejected: errors would go unchecked into the docs agents trust).

## Trade-offs accepted

Kyle reviews `pending-updates.md` regularly. Runs only when the Mac is awake with the desktop app open; 17:00 was chosen because the laptop isn't reliably on at 20:00, and catch-up makes missed days harmless. Whether a scheduled task can write Project knowledge is still to be checked; the fallback is a sync step at the start of each session.

## Workflow detail

Review pending updates at the start of a session with Claude; apply approved edits and bump `version`/`last_verified`.

## Related notes

- [[knowledge-architecture]]
- [[2026-10-23-001]]
- [[adopt-repo-vault-ownership-split-for-project-knowledge]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[adopt-frontmatter-lifecycle-schema]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[retire-obsidian-llm-wiki-plugin]]
- [[scope-agent-context-per-tool]]
- [[version-the-vault-with-git]]
- [[defer-postman-suite-ci-until-suite-split]]
