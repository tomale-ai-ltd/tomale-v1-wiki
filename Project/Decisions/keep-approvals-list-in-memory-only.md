---
type: decision
title: "keep-approvals-list-in-memory-only"
project: tomale-rn-v1
status: proposed
date: "2026-11-19"
related:
  - "[[2026-11-19-001]]"
  - "[[surface-approvals-on-parent-home-and-avatar-menu]]"
  - "[[wait-for-server-on-profile-changes]]"
  - "[[hide-rejected-stories-from-child]]"
affects:
  - "specs/010-approvals/plan.md"
features:
  - F-parental-oversight
---

# Decision: keep-approvals-list-in-memory-only

## What we decided

In slice 010, `approvalsStore` is memory only (Zustand without persist), recorded as a Principle 4 exception in the 010 plan. It does not reuse `StoriesStore`. The approvals count is `awaiting.length`. `approvalsStore.reset()` runs on profile switch and on sign-out (`store/AuthStore.ts` `signOut`).

## Why

From the 010 plan (19/11): the server decides `approval_state`, so a saved awaiting list could show a story the parent already decided, and could show a count on a child profile.

## Alternatives considered

Reusing `StoriesStore`: rejected in the plan because that store is persisted under `stories`.

## Trade-offs accepted

No offline approvals cache; the list is fetched again rather than read from disk. The plan sets the sunset as this slice and says to revisit if a later spec asks for an offline approvals cache.

## Workflow detail

The constitution is not edited; the exception lives in the 010 plan's Complexity Tracking. The reset calls on profile switch and sign-out were set by Kyle in the task edits.

## Related notes

[[2026-11-19-001]], [[surface-approvals-on-parent-home-and-avatar-menu]], [[wait-for-server-on-profile-changes]], [[hide-rejected-stories-from-child]], [[PRD-Parental-Oversight-Content-Approval]]
