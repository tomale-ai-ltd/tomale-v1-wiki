---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Two approvals bug fixes, not pushed

## What changed
- `e5b8c76` Ignore a story list that arrives after the profile has changed. `reset()` bumps a generation, and a load writes only if that generation is still current.
- `e93b2d8` Record the picker cover after the main layout renders.
- `pnpm check` passed. `pnpm test`: 18 suites, 114 tests passed. Not pushed.

## Decisions
- A stale failure is dropped the same way as a stale list, so it cannot set an error on the next profile.

## Open questions / blockers
- Not checked on the phone. Metro and the simulator were left running.

## Next
- Kyle's phone test list.
