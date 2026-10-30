---
type: decision
title: limit-xano-knowledge-to-locked-agents-md
project: tomale-rn-v1
status: accepted
date: "2026-10-30"
related:
  - "[[2026-10-30-001]]"
  - "[[scope-agent-context-per-tool]]"
  - "[[track-agent-context-copies-by-fingerprint]]"
  - "[[backend-xano]]"
affects:
  - "[[knowledge-architecture]]"
  - "[[backend-xano]]"
  - "[[agent-context-sync]]"
features:
  - X-process
---

# Decision: limit-xano-knowledge-to-locked-agents-md

## What we decided

Xano Knowledge holds AGENTS.md only, locked, as a verbatim copy of [[backend-xano]] §3. No Knowledge docs or skills unless a repeated mistake justifies one.

## Why

Avoid admin load and diverging copies.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Kyle pasted and locked AGENTS.md on 30/10. [[backend-xano]] §3 gained the full error-type rules after Xano's own draft exposed the gap. When §3 changes, the pipeline flags it via [[agent-context-sync]] and Kyle re-pastes the block.

## Related notes

- [[2026-10-30-001]]
- [[scope-agent-context-per-tool]]
- [[track-agent-context-copies-by-fingerprint]]
- [[backend-xano]]
- [[agent-context-sync]]
