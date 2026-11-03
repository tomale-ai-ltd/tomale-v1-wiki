---
type: decision
title: "split-queues-into-one-note-per-item-with-bases"
project: tomale-rn-v1
status: accepted
date: "2026-11-01"
related:
  - "[[2026-11-01-001]]"
affects:
  - "[[operating-model]]"
  - "[[knowledge-architecture]]"
  - "[[agent-context-sync]]"
  - "[[repo-sync]]"
  - "[[pending-updates]]"
features:
  - X-process
---

# Decision: split-queues-into-one-note-per-item-with-bases

## What we decided

The repo-sync and pending-updates queues become one note per item: `Canonical/repo-sync/` and `Canonical/pending-updates/` hold one note each (properties: id, title, status, class/batch/target/source, date). `repo-sync.base` and `pending-updates.base` show Open/Done tables embedded in the hub notes `repo-sync.md` and `pending-updates.md`. Kyle approves by editing the Status cell.

## Why

The single-file queues were hard to read and approve.

## Alternatives considered

Tidy the single file with a summary table (rejected: still edit-in-text).

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Migrated 23 RS and 3 PU items by script; new templates `Templates/repo-sync-item.md` and `Templates/pending-update.md`. Applied in session (approved by Kyle): [[operating-model]] 1.2, [[knowledge-architecture]] 1.2, [[agent-context-sync]] 1.1, both hub notes 2.0; daily pipeline and weekly check prompts updated; RS-2026-11-01-05 (Cursor rule) reworded.

## Related notes

- [[2026-11-01-001]]
- [[repo-sync]]
- [[pending-updates]]
- [[knowledge-architecture]]
