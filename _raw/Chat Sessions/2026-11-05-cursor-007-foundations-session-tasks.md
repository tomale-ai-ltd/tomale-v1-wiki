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

## Amendment 2026-11-05
- Kyle: a refresh timeout or HTTP 429 must not sign the parent out. Same as a network error or a 5xx: stay signed in, keep issuedAt, show the action's error.
- Updated FR-012 and the matching spec sentences, plan.md, T012 (429 moved out of the sign-out cases; Jest cases added for timeout and 429), plus research, data model, session contract, and quickstart so they do not still say 429 signs the parent out. No code implemented.
- Applied analyze remediations in spec.md, plan.md, and tasks.md only. Foreground refresh stays the 50-minute rule; plan records RS-2026-11-05-02 for a constitution clarification after merge. Stay-signed-in set is network error, timeout, 429, and 5xx. FR-001 stores session id only when the body includes it. Account creation is out of this slice. Added T014 for secure-session storage tests and renumbered through T026. T013 signOut clears Sentry identity. Removed the incorrect parallel markers. No app code.
