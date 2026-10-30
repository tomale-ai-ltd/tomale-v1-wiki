---
type: decision
title: sync-project-knowledge-by-hash-manifest
project: tomale-rn-v1
status: accepted
date: "2026-10-30"
related:
  - "[[2026-10-30-001]]"
  - "[[scope-agent-context-per-tool]]"
  - "[[add-propose-only-reconcile-and-staleness-automations]]"
  - "[[agent-context-sync]]"
affects:
  - "[[knowledge-architecture]]"
  - "[[agent-context-sync]]"
features:
  - X-process
---

# Decision: sync-project-knowledge-by-hash-manifest

## What we decided

Claude Project knowledge mirrors `Canonical/`, all of `Project/Decisions/`, the constitution and the data model. The daily pipeline keeps it in sync using a hash manifest (`Project/Automation/project-sync-manifest.json`). The April hand-uploaded docs are retired: 37 were deleted and 162 current docs uploaded in B11 (30/10), and the Project instructions were rewritten.

## Why

Not discussed in session notes beyond the B11 test: a scheduled task was tested and can write Project knowledge, so the sync can run unattended.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

The daily pipeline compares each mirrored file's hash with the manifest, uploads new or changed files, deletes docs whose source no longer exists, and writes the manifest back.

## Related notes

- [[2026-10-30-001]]
- [[scope-agent-context-per-tool]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[agent-context-sync]]
- [[knowledge-architecture]]
