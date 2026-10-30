---
type: living-doc
title: agent-context-sync
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-30
last_verified: 2026-10-30
owner: vault
related:
  - "[[knowledge-architecture]]"
  - "[[backend-xano]]"
  - "[[scope-agent-context-per-tool]]"
---

# Agent context sync

Each rule has one home. Other agents get a copy of it, or a pointer to it, never a separately written version. This note lists the hand-maintained copies and records the fingerprint of the source at the time each copy was last updated. The daily pipeline compares fingerprints and raises an item in [[pending-updates]] when a source has changed ([[knowledge-architecture]] §10).

| Copy | Source (single home) | How it's updated | Fingerprint method |
|---|---|---|---|
| Claude Project knowledge | `Canonical/`, `Project/Decisions/`, constitution, data model | Automatically by the daily pipeline (or at session start if a scheduled task can't write Project knowledge) | n/a |
| Xano Knowledge → AGENTS.md (locked) | [[backend-xano]] §3, the block between `<!-- xano-agents:start -->` and `<!-- xano-agents:end -->` | Kyle pastes the block verbatim | `sed -n '/xano-agents:start/,/xano-agents:end/p' Canonical/backend-xano.md \| sha256sum`, first 12 characters |
| Cursor `.cursor/rules/tomale-api.mdc` | Constitution (app-side rules: secure storage, 401 interceptor, error codes, pence) | Cursor via a repo-sync item | `sha256sum` of `~/Developer/tomale/tomale-rn-test/.specify/memory/constitution.md`, first 12 characters |
| Cursor `.cursor/rules/tomale-project.mdc` | [[knowledge-architecture]] §11 (Cursor row) | Cursor via a repo-sync item | Not tracked (rarely changes) |

## Recorded fingerprints

| Copy | Fingerprint at last update | Updated |
|---|---|---|
| Xano AGENTS.md | cce702f9f98b | 2026-10-30 (pasted by Kyle, locked) |
| Cursor tomale-api.mdc | 3ccb0a3496c9 (constitution 1.5.1) | 2026-10-30 (PR #11) |

## Pipeline rule

For each tracked copy: compute the source fingerprint. If it differs from the recorded one and [[pending-updates]] has no open item for that copy, add a `PU-` item (Target: the copy; Proposed change: "source changed, fingerprint <new>" plus the action; Status: proposed). Actions: Xano: "paste the §3 block of backend-xano.md into Xano Knowledge → AGENTS.md"; Cursor: "queue a repo-sync item to review tomale-api.mdc against the constitution". When Kyle sets the item's Status to `applied`, the pipeline records that fingerprint and date in the table above. Recording fingerprints here is the one edit the pipeline may make to this note.
