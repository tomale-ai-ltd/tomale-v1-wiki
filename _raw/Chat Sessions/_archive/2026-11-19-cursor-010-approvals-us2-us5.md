---
date: 2026-11-19
source: cursor
branch: 010-approvals
feature: 010-approvals
---

# Approvals US2 through polish, not pushed

## What changed
- `7ac2fe0` Show a child a locked waiting card instead of the story.
- `d5d62a7` Let a parent reject a story, then keep it, give it back, or delete it.
- `c970c04` Hold an approvals, Store, or Settings link until a parent is in.
- `a4bfffe` Add the home shortcuts and an empty favourites row.
- `47df78f` Record the approvals phone checks after the automated run.
- Not pushed. T017, T023, T025, and T027 are marked not shot: Kyle tests on the phone.
- `pnpm check` passed. `pnpm test`: 18 suites, 113 tests passed.

## Decisions
- Cursor stopped at T028. T029 stays for Kyle.
- The waiting sheet and the rejected sheets draw no story picture. The character tile uses an icon, not the board's dragon.
- Closing the picker clears a remembered link, along with picking another profile, closing the PIN pad, and changing tab.
- Delete confirmation has "Keep it", which sends nothing.

## Open questions / blockers
- Nothing was checked on the phone or the simulator. Metro and the simulator were left running.

## Next
- Kyle walks the phone test list in `specs/010-approvals/tasks.md`.
