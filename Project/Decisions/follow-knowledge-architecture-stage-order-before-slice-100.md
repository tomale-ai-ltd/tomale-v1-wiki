---
type: decision
title: follow-knowledge-architecture-stage-order-before-slice-100
project: tomale-rn-v1
status: accepted
date: 2026-10-24
related:
  - "[[2026-10-24-001]]"
  - "[[knowledge-architecture]]"
affects:
  - "[[knowledge-architecture]]"
---

# Decision: follow-knowledge-architecture-stage-order-before-slice-100

## What we decided

The knowledge restructure follows the approved [[knowledge-architecture]] §13 stage order (B6 → B12) in full before the frontend resumes at Slice 100. Claude's proposed "critical path to Slice 100" shortcut was not adopted (25/10, 00:23).

## Why

Not discussed in session notes.

## Alternatives considered

A "critical path to Slice 100" shortcut proposed by Claude (not adopted).

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Order after `b5-frontmatter` is merged: B6 generated specs (data-model script, OpenAPI refresh, `webhooks` export) → B7 V1 audit → B8 canonical docs → B9 PRDs → B10 repo sync (RS-01 to RS-06, incl. pnpm) → B11 agent access and automations → B12 close-out. Slice 100 (speckit 007) then starts after the `wip/` branch is resolved into `main`.

## Related notes

- [[2026-10-24-001]]
- [[knowledge-architecture]]
- [[operating-model]]
- [[promote-pnpm-migration-ahead-of-slice-100]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[classify-and-batch-repo-sync-changes]]
- [[2-build-plan]]
