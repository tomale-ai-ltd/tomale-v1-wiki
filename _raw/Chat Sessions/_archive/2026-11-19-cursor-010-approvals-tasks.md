---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Tasks for approvals

## What changed
- Added `specs/010-approvals/tasks.md` (uncommitted). Kyle asked for `/speckit.tasks` with the store, pending route, and refusal mapping before any screen, picture data named on each screen task, one screenshot task after each user story, and a phone list at the end.
- No code, no Metro, no simulator, no push.

## Decisions
- Kyle set the task shape: foundations first, `pnpm shot` once per board state on the simulator he already has running, no re-shoots, a failed shot is noted, differences split into bugs and snags.
- Cursor put the pure row and picture rules and `StoryCover` in the foundational phase as well, because the screens depend on them and they are not screens.
- US4 has no board, so its screenshot task records that and does not shoot. US5 compares the Home shots already taken for the tiles and favourites.

## Open questions / blockers
- None.

## Next
- Kyle reviews `tasks.md`, then `/speckit.analyze` when he wants it. Implementation has not started.
