---
type: decision
title: "hide-rejected-stories-from-child"
project: tomale-rn-v1
status: accepted
date: "2026-11-12"
related:
  - "[[2026-11-12-001]]"
  - "[[m3-approvals-backend-prep-brief]]"
  - "[[per-child-story-visibility]]"
affects:
  - "[[PRD-Parental-Oversight-Content-Approval]]"
  - "GET /instant_stories"
features:
  - F-parental-oversight
---

# Decision: hide-rejected-stories-from-child

## What we decided
Kyle, 12/11: a story the parent rejects is hidden from the child, with no "not this one" card. The child sees their own awaiting stories as redacted "waiting" cards; once rejected, the card disappears. The parent can delete the rejected story or move it to their own profile (assign, M3 part A).

## Why
Not discussed in session notes.

## Alternatives considered
A "not this one" card shown to the child after rejection.

## Trade-offs accepted
Not discussed in session notes.

## Workflow detail
Built in M3 part B, change set B5: `GET /instant_stories` for a child returns awaiting cards `{id, title, approval_state: "awaiting", created_at}` and never rejected stories; the parent list takes an optional `approval_state` filter (`awaiting` | `rejected`) for the inbox and the rejected list. Postman folder 7 checks that the child's card disappears after a reject.

## Related notes
[[m3-approvals-backend-prep-brief]], [[m3-approvals-xano-prompts]], [[PRD-Parental-Oversight-Content-Approval]], [[per-child-story-visibility]]
