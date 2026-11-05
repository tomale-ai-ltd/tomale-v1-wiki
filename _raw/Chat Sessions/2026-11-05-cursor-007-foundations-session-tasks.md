---
date: 2026-11-05
source: cursor
branch: 007-foundations-session
feature: 007-foundations-session
---

# Tasks for 007 client session handling

## What changed
- Wrote `specs/007-foundations-session/tasks.md` from the plan, spec, research, data model, session contract, and quickstart. 25 tasks, T001–T025. Nothing committed. Implementation has not started.

## Decisions
- Jest tasks are included because the plan, quickstart, and constitution require automated auth checks. US3 persistence stays a device check.
- The `@swc/helpers` override is an explicit non-change until 2026-11-11.

## Open questions / blockers
- None for the task list. `active_profile.id` is still read with a type guard.

## Next
- Implement when Kyle asks, starting at T001. MVP stops after User Story 1 if he wants that checkpoint.
