---
type: decision
title: resume-frontend-at-slice-100
project: tomale-rn-v1
status: accepted
date: 2026-10-30
supersedes:
  - "[[place-frontend-development-on-hold]]"
related:
  - "[[roadmap]]"
  - "[[knowledge-architecture]]"
  - "[[follow-knowledge-architecture-stage-order-before-slice-100]]"
affects:
  - "[[CURRENT]]"
  - "[[roadmap]]"
features:
  - X-process
---

# Decision: resume-frontend-at-slice-100

## What we decided

Frontend development resumes, ending the hold from 27/12/2025. The order is the [[roadmap]]: M1 (app foundations rework) first, then backend prep for Characters, then **Slice 100 = speckit 007** ([[PRD-Characters]]). All app work branches from and merges into `main`; the `wip/pre-restructure-2026-10-24` branch is retired once merged.

## Why

The reasons for the hold are resolved:
- Phase 1 security and data integrity signed off on 23/10 (86/86 `_tests`): authenticated endpoints, ownership-scoped queries, soft deletes, webhook verification.
- The knowledge restructure (B0–B12) is complete: canonical docs, reconciled PRDs with backend prep, generated data model and API contract, constitution 1.5.1, pnpm with dependency auditing in CI, automated knowledge pipeline.

## Alternatives considered

- Keep the hold until more backend work (entitlements, PIN gate) is built: rejected; the roadmap interleaves backend prep with each slice, and the January launch date needs frontend progress now ([[move-v1-public-launch-to-late-january]]).

## Trade-offs accepted

Backend items for later milestones (entitlements, PIN, approvals, RevenueCat) are still to build; each slice's backend prep is done just before it.

## Workflow detail

Speckit per slice (`/speckit.specify` can take the micro-PRD, RS-2026-10-29-01); Cursor writes a raw session note per session; PRs into `main` must pass CI.

## Related notes

- [[place-frontend-development-on-hold]]
- [[roadmap]]
- [[CURRENT]]
