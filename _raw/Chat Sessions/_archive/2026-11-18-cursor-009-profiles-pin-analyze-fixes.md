---
date: 2026-11-18
source: cursor
branch: 009-profiles-pin
feature: 009-profiles-pin
---

# Analysis fixes for profiles and PIN

## What changed
- Applied the analysis edits in `spec.md`, `plan.md`, `data-model.md`, and `tasks.md`. Profile list is persisted. The 15-minute clock is not. Create, rename, picture change, and delete wait for the server. Copy matches the boards. A switch `PROFILE_NOT_FOUND` stays on the picker. No implementation. No commit.

## Decisions
- Kyle asked for every proposed edit, and widened the optimistic-UI exception to every profile change because a refused name must not appear even briefly. Cursor recorded that as the third Complexity Tracking row, sunset this slice.

## Open questions / blockers
- None from the second analysis pass.

## Next
- Implement when Kyle asks.
