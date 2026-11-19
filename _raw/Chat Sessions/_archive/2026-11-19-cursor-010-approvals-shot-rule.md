---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Rejected-action shots only if a story is already rejected

## What changed
- In `specs/010-approvals/tasks.md`, T023 now shoots `010-rejected-actions` and `010-rejected-delete` only when a rejected story is already on the device. The delete ask is opened and shot, and never confirmed. Otherwise the task notes "not shot" and continues.

## Decisions
- Kyle set that rule.

## Open questions / blockers
- None.

## Next
- Kyle reviews the task list.
