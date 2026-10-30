---
type: decision
title: track-agent-context-copies-by-fingerprint
project: tomale-rn-v1
status: accepted
date: "2026-10-30"
related:
  - "[[2026-10-30-001]]"
  - "[[agent-context-sync]]"
  - "[[limit-xano-knowledge-to-locked-agents-md]]"
  - "[[scope-agent-context-per-tool]]"
affects:
  - "[[agent-context-sync]]"
  - "[[knowledge-architecture]]"
features:
  - X-process
---

# Decision: track-agent-context-copies-by-fingerprint

## What we decided

Hand-maintained agent context copies are tracked by fingerprint in [[agent-context-sync]]. Each rule has one home. The pipeline raises a pending-updates item when a source changes and records the fingerprint when Kyle marks it applied.

## Why

Not discussed in session notes beyond the principle that each rule has one home (other agents get a copy or a pointer, never a separately written version).

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Tracked copies are the Xano AGENTS.md (source: [[backend-xano]] §3) and Cursor `tomale-api.mdc` (source: the constitution). Kyle applies the copy and sets the [[pending-updates]] item to applied; the pipeline then records the new fingerprint and date.

## Related notes

- [[2026-10-30-001]]
- [[agent-context-sync]]
- [[limit-xano-knowledge-to-locked-agents-md]]
- [[scope-agent-context-per-tool]]
- [[pending-updates]]
